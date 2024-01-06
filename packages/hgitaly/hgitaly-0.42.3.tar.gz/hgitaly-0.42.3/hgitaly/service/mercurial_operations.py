# Copyright 2023 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from grpc import StatusCode
import logging

from mercurial.merge import merge
from mercurial.phases import (
    public as PUBLIC,
)

from .. import message
from ..changelog import (
    ancestor,
    merge_content,
)
from ..logging import LoggerAdapter
from ..revision import (
    gitlab_revision_changeset,
)

from ..stub.mercurial_operations_pb2 import (
    MergeAnalysisRequest,
    MergeAnalysisResponse,
)
from ..stub.mercurial_operations_pb2_grpc import (
    MercurialOperationsServiceServicer,
)
from ..servicer import HGitalyServicer

base_logger = logging.getLogger(__name__)

MERGE_CONFLICTS_LABELS = [b'working copy', b'merge rev', b'common ancestor']


class MercurialOperationsServicer(MercurialOperationsServiceServicer,
                                  HGitalyServicer):
    """MercurialOperationService implementation.

    The ordering of methods in this source file is the same as in the proto
    file.
    """
    def MergeAnalysis(self,
                      request: MergeAnalysisRequest,
                      context) -> MergeAnalysisResponse:
        logger = LoggerAdapter(base_logger, context)
        repo = self.load_repo(request.repository, context)
        source_cs = gitlab_revision_changeset(repo, request.source_revision)
        if source_cs is None:
            context.abort(
                StatusCode.INVALID_ARGUMENT,
                "Source revision %r not found" % request.source_revision)
        target_cs = gitlab_revision_changeset(repo, request.target_revision)
        if target_cs is None:
            context.abort(
                StatusCode.INVALID_ARGUMENT,
                "Target revision %r not found" % request.target_revision)

        source_branch = source_cs.branch()
        target_branch = target_cs.branch()
        logger.info("Merge Analysis: source branch %r, target branch %r",
                    source_branch, target_branch)
        is_ff = (ancestor(source_cs, target_cs) == target_cs.rev()
                 and source_branch == target_branch)

        has_obsolete = has_unstable = False
        for cs in merge_content(source_cs, target_cs):
            if not has_obsolete:
                has_obsolete = cs.obsolete()
            if not has_unstable:
                has_unstable = cs.isunstable()
            if has_obsolete and has_unstable:
                break

        has_conflicts = False
        if not (is_ff
                or has_obsolete or has_unstable
                or request.skip_conflicts_check):
            with self.working_dir(gl_repo=request.repository,
                                  repo=repo,
                                  context=context,
                                  changeset=target_cs) as wd:
                has_conflicts = not wd_merge(wd, source_cs)

        res = MergeAnalysisResponse(
            is_fast_forward=is_ff,
            has_obsolete_changesets=has_obsolete,
            has_unstable_changesets=has_unstable,
            has_conflicts=has_conflicts,
            target_is_public=target_cs.phase() == PUBLIC,
            target_node_id=target_cs.hex().decode('ascii'),
            target_branch=target_cs.branch(),
            target_topic=target_cs.topic(),
            source_node_id=source_cs.hex().decode('ascii'),
            source_branch=source_cs.branch(),
            source_topic=source_cs.topic(),
        )
        logger.info("MergeAnalysis result %r", message.Logging(res))
        return res


def wd_merge(working_dir, source_cs):
    """Merge source_cs in the given a working directory (repo share).

    :source_cs: a :class:`changectx`, usually not tied to ``working_dir`` but
      to its share source or a share sibling.
    :return: whether it suceeded
    """
    # re-evalutate the changectx in the context of working_dir,
    # as `merge()` will read the repo from it
    repo = working_dir.repo
    source_for_wd = repo[source_cs.rev()]

    overrides = {(b'ui', b'forcemerge'): b'internal:merge3',
                 (b'ui', b'interactive'): b'off'}
    with repo.ui.configoverride(overrides, b'merge'):
        # not sure labels are really necessary, but it is
        # possible that the merge tools require them.
        stats = merge(source_for_wd,
                      labels=MERGE_CONFLICTS_LABELS)
        return not stats.unresolvedcount
