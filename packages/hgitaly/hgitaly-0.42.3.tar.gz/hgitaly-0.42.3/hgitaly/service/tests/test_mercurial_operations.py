# Copyright 2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from grpc import (
    RpcError,
    StatusCode,
)
import pytest

from hgitaly.stub.mercurial_operations_pb2 import (
    MergeAnalysisRequest,
    MergeAnalysisResponse,
)
from hgitaly.stub.mercurial_operations_pb2_grpc import (
    MercurialOperationsServiceStub,
)

from .fixture import ServiceFixture


class OperationsFixture(ServiceFixture):

    stub_cls = MercurialOperationsServiceStub

    def merge_analysis(self, **kw):
        return self.stub.MergeAnalysis(MergeAnalysisRequest(
            repository=self.grpc_repo, **kw))


@pytest.fixture
def operations_fixture(grpc_channel, server_repos_root):
    with OperationsFixture(grpc_channel, server_repos_root) as fixture:
        yield fixture


def test_merge_analysis_ff(operations_fixture):
    repo_wrapper = operations_fixture.repo_wrapper
    commit_file = repo_wrapper.commit_file
    default_ctx = commit_file('foo')
    default_sha = default_ctx.hex().decode()
    topic_ctx = commit_file('foo', parent=default_ctx, topic='zetop')
    topic_first_hex = topic_ctx.hex()
    topic_first_sha = topic_first_hex.decode()

    merge_analysis = operations_fixture.merge_analysis
    assert (
        merge_analysis(source_revision=b'topic/default/zetop',
                       target_revision=b'branch/default')
        ==
        MergeAnalysisResponse(is_fast_forward=True,
                              source_node_id=topic_first_sha,
                              source_branch=b'default',
                              source_topic=b'zetop',
                              target_node_id=default_sha,
                              target_branch=b'default',
                              target_topic=b'',
                              target_is_public=False,
                              )
    )
    newtop_sha = commit_file('foo',
                             parent=topic_ctx,
                             topic='newtop').hex().decode()
    repo_wrapper.update(topic_ctx)
    repo_wrapper.amend_file('foo').hex()

    assert (
        merge_analysis(source_revision=b'topic/default/newtop',
                       target_revision=b'branch/default')
        ==
        MergeAnalysisResponse(is_fast_forward=True,
                              has_obsolete_changesets=True,
                              has_unstable_changesets=True,
                              source_node_id=newtop_sha,
                              source_branch=b'default',
                              source_topic=b'newtop',
                              target_node_id=default_sha,
                              target_branch=b'default',
                              target_topic=b'',
                              target_is_public=False,
                              )
    )
    assert (
        merge_analysis(source_revision=topic_first_hex,
                       target_revision=b'branch/default')
        ==
        MergeAnalysisResponse(is_fast_forward=True,
                              has_obsolete_changesets=True,
                              has_unstable_changesets=False,
                              source_node_id=topic_first_sha,
                              source_branch=b'default',
                              source_topic=b'zetop',
                              target_node_id=default_sha,
                              target_branch=b'default',
                              target_topic=b'',
                              target_is_public=False,
                              )
    )

    # error cases
    with pytest.raises(RpcError) as exc_info:
        merge_analysis(source_revision=b'unknown',
                       target_revision=b'branch/default')
    assert exc_info.value.code() == StatusCode.INVALID_ARGUMENT
    assert 'source revision' in exc_info.value.details().lower()

    with pytest.raises(RpcError) as exc_info:
        merge_analysis(source_revision=b'topic/default/zetop',
                       target_revision=b'unknownn')
    assert exc_info.value.code() == StatusCode.INVALID_ARGUMENT
    assert 'target revision' in exc_info.value.details().lower()


def test_merge_analysis_conflict(operations_fixture):
    repo_wrapper = operations_fixture.repo_wrapper
    commit_file = repo_wrapper.commit_file
    ctx0 = commit_file('foo')
    default_sha = commit_file('foo', content="default").hex().decode()
    repo_wrapper.set_phase('public', ['.'])  # also testing `target_is_public`
    topic_first_sha = commit_file('foo', parent=ctx0,
                                  topic='zetop', content="top"
                                  ).hex().decode()

    merge_analysis = operations_fixture.merge_analysis
    assert (
        merge_analysis(source_revision=b'topic/default/zetop',
                       target_revision=b'branch/default')
        ==
        MergeAnalysisResponse(is_fast_forward=False,
                              has_conflicts=True,
                              source_node_id=topic_first_sha,
                              source_branch=b'default',
                              source_topic=b'zetop',
                              target_node_id=default_sha,
                              target_branch=b'default',
                              target_topic=b'',
                              target_is_public=True,
                              )
    )

    # same without the conflicts check
    conflicts_check_skipped = merge_analysis(
        skip_conflicts_check=True,
        source_revision=b'topic/default/zetop',
        target_revision=b'branch/default',
    )
    assert conflicts_check_skipped.is_fast_forward is False
    assert conflicts_check_skipped.has_conflicts is False  # was really skipped

    # solving the conflict
    topic_fixed_sha = commit_file('foo', topic='zetop',
                                  content="default").hex().decode()
    assert (
        merge_analysis(source_revision=b'topic/default/zetop',
                       target_revision=b'branch/default')
        ==
        MergeAnalysisResponse(is_fast_forward=False,
                              has_conflicts=False,
                              source_node_id=topic_fixed_sha,
                              source_branch=b'default',
                              source_topic=b'zetop',
                              target_node_id=default_sha,
                              target_branch=b'default',
                              target_topic=b'',
                              target_is_public=True,
                              )
    )
