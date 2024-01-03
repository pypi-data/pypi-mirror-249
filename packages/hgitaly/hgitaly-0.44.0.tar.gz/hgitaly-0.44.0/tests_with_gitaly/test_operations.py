# Copyright 2023 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Tests for OperationService (most mutations)

Because it is not convenient to mutate the Mercurial and Git repositories
Without side-effects, these tests are mostly checking assumptions on the
behaviour of Gitaly
"""
from pathlib import Path
import pytest
from hgitaly.stub.shared_pb2 import User

from hgitaly.stub.operations_pb2 import (
    OperationBranchUpdate,
    UserFFBranchRequest,
    UserSquashRequest,
)
from hgitaly.stub.operations_pb2_grpc import (
    OperationServiceStub,
)

from . import skip_comparison_tests
if skip_comparison_tests():  # pragma no cover
    pytestmark = pytest.mark.skip

parametrize = pytest.mark.parametrize

TESTS_DATA_DIR = Path(__file__).parent / 'data'
TIP_TAG_NAME = b'tip'


@pytest.fixture
def comparison(gitaly_comparison):
    gitaly_comparison.user = User(gl_id='user-37',
                                  name=b'Test User',
                                  email=b'testuser@heptapod.test',
                                  gl_username='testuser')
    yield gitaly_comparison


def test_compare_squash(comparison):
    """This test is mostly about error cases, as comparing the """
    fixture = comparison
    git_repo = fixture.git_repo
    wrapper = fixture.hg_repo_wrapper

    gl_branch = b'branch/default'
    gl_topic = b'topic/default/sampletop'
    wrapper.write_commit('foo')
    wrapper.write_commit('zoo', topic='sampletop')
    wrapper.write_commit('bar')

    rpc_helper = fixture.rpc_helper(stub_cls=OperationServiceStub,
                                    method_name='UserSquash',
                                    request_cls=UserSquashRequest,
                                    request_defaults=dict(
                                        user=fixture.user,
                                        author=fixture.user,
                                        commit_message=b'squashed'),
                                    request_sha_attrs=['start_sha', 'end_sha'])
    assert_compare_errors = rpc_helper.assert_compare_errors
    # proof that any valid revspec can be passed as "sha" arguments
    git_resp = rpc_helper.call_git_only(start_sha=gl_branch, end_sha=gl_topic)
    squashed_sha = git_resp.squash_sha
    # Gitaly does not move the ref, apparently
    assert git_repo.commit_hash_title(squashed_sha) == [
        squashed_sha.encode('ascii'),
        b'squashed'
    ]

    # revision resolution errors
    assert_compare_errors(start_sha='unresolvable', end_sha=gl_topic)
    assert_compare_errors(start_sha=gl_branch, end_sha='unresolvable')

    # errors on missing arguments
    assert_compare_errors(start_sha=gl_topic)
    assert_compare_errors(end_sha=gl_topic)
    assert_compare_errors(user=None, start_sha=gl_branch, end_sha=gl_topic)
    assert_compare_errors(commit_message=None,
                          start_sha=gl_branch, end_sha=gl_topic)
    assert_compare_errors(author=None, start_sha=gl_branch, end_sha=gl_topic)


def test_compare_ff_branch(comparison):
    """This test is mostly about error cases, as comparing the """
    fixture = comparison
    git_repo = fixture.git_repo
    wrapper = fixture.hg_repo_wrapper

    gl_branch = b'branch/default'
    gl_topic = b'topic/default/sampletop'
    ctx0 = wrapper.write_commit('foo')
    sha0 = ctx0.hex()
    sha1 = wrapper.write_commit('foo').hex()
    ctx2 = wrapper.write_commit('zoo', topic='sampletop')
    sha2 = ctx2.hex()
    git_sha2 = git_repo.branches()[gl_topic]['sha']
    ctx_old = wrapper.write_commit('old', parent=ctx0, topic='needs-rebase')

    rpc_helper = fixture.rpc_helper(
        stub_cls=OperationServiceStub,
        method_name='UserFFBranch',
        error_details_normalizer=lambda s, **kw: s.lower(),
        request_cls=UserFFBranchRequest,
        request_defaults=dict(user=fixture.user),
        request_sha_attrs=['commit_id',
                           'expected_old_oid'],
    )
    assert_compare = rpc_helper.assert_compare
    assert_compare_errors = rpc_helper.assert_compare_errors

    # A working Gitaly call, as a baseline that cannot be directly compared.
    git_resp = rpc_helper.call_git_only(branch=gl_branch,
                                        commit_id=sha2,
                                        expected_old_oid=sha1,
                                        )
    assert git_resp.branch_update == OperationBranchUpdate(
        commit_id=git_sha2,
        repo_created=False,
        branch_created=False,
    )
    assert git_repo.commit_hash_title('branch/default')[0] == git_sha2

    # revision resolution errors
    unknown_sha = '2134cafe' * 5
    assert_compare_errors(commit_id=unknown_sha,
                          expected_old_oid=sha0.decode(),
                          branch=gl_branch)
    assert_compare_errors(commit_id='not-an-id',
                          same_details=False,
                          expected_old_oid=sha0.decode(),
                          branch=gl_branch)
    assert_compare_errors(commit_id=sha2,
                          same_details=False,
                          expected_old_oid='not-an-id',
                          branch=gl_branch)
    assert_compare_errors(commit_id=sha2,
                          expected_old_oid=unknown_sha,
                          branch=gl_branch)

    # expected_old_oid mismatch
    assert_compare(commit_id=sha2,
                   expected_old_oid=sha0,
                   branch=gl_branch)

    # errors on missing arguments
    assert_compare_errors(commit_id=sha2)
    assert_compare_errors(user=None, branch=gl_branch, commit_id=sha2)

    # Not a fast-forward
    assert_compare_errors(commit_id=ctx_old.hex().decode(),
                          branch=gl_branch)
