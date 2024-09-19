"""Test ngcp-logic-engine REST API."""

import difflib
from collections import Counter

from fastapi import status
from fastapi.testclient import TestClient

from ngcp_logic_engine import config
from ngcp_logic_engine.api import api_v1, app
from ngcp_logic_engine.redismanager import RedisManager

app.include_router(api_v1)
prefix = "/api/v1/dialog"
client = TestClient(app)

mock_dialog = {
    "callid": "8fasnef81iu2jnfdojqwefhouf",
    "ftag": "$12312312$",
    "ttag": "$ttag232421$",
}

mock_dialog_no_tag = {
    "callid": "8fasnef81iu2jnfdojqwefhouf",
}

mock_dialog_uuid = mock_dialog["callid"]
if config.settings.use_dialog_id_tags:
    mock_dialog_uuid = f"{mock_dialog['ftag']}:{mock_dialog['callid']}:{mock_dialog['ttag']}"

mock_dialog_bundle = {"dialog": mock_dialog}

mock_call_counter_dialog_params = {
    "dialog": mock_dialog,
    "counter": "user",
    "id": "iufasdifj23",
}

mock_call_counter_dialog_params_no_id = {
    "dialog": mock_dialog,
    "counter": "user",
}

mock_invalid_counter_dialog_params = {
    "dialog": mock_dialog,
    "counter": "invalid",
    "id": "iufasdifj23",
}

mock_general_counter_dialog_params = {
    "dialog": mock_dialog,
    "counter": "peer:faxserver",
}

mock_peer_dialog_params = {
    "dialog": mock_dialog,
    "peer_id": "fi234908r",
}

mock_caller_dialog_params = {
    "dialog": mock_dialog,
    "p_to_group": 0,
    "user_id": "iufasdifj23",
    "account_id": "29ru-q9wjr42",
    "reseller_id": "kaskldfhjl4",
    "location_id": "p28u348qwfn",
}

mock_callee_dialog_params = {
    "dialog": mock_dialog,
    "p_to_group": 0,
    "user_id": "iufasdifj23",
    "account_id": "29ru-q9wjr42",
    "reseller_id": "kaskldfhjl4",
    "location_id": "p28u348qwfn",
    "callee_ip": "192.111.135",
}

mock_active_user_dialog_params = {
    "dialog": mock_dialog,
    "user_id": "iufasdifj23",
}

mock_no_tag_dialog_params = {
    "dialog": mock_dialog_no_tag,
    "user_id": "iufasdifj23",
}

mock_user_dialog_bundle = {
    "dialog": mock_dialog,
    "dialog_key_ids": {
        "user": "iufasdifj23",
    },
}

mock_account_dialog_bundle = {
    "dialog": mock_dialog,
    "dialog_key_ids": {
        "account": "29ru-q9wjr42",
    },
}

mock_location_dialog_bundle = {
    "dialog": mock_dialog,
    "dialog_key_ids": {
        "location": "p28u348qwfn",
    },
}

mock_reseller_dialog_bundle = {
    "dialog": mock_dialog,
    "dialog_key_ids": {
        "reseller": "kaskldfhjl4",
    },
}

mock_peer_dialog_bundle = {
    "dialog": mock_dialog,
    "dialog_key_ids": {
        "peer": "fi234908r",
    },
}

mock_callee_dialog_bundle = {
    "dialog": mock_dialog,
    "dialog_key_ids": {
        "user": "iufasdifj23",
        "account": "29ru-q9wjr42",
        "location": "p28u348qwfn",
    },
}

mock_caller_dialog_bundle = {
    "dialog": mock_dialog,
    "dialog_key_ids": {
        "user": "iufasdifj23",
        "account": "29ru-q9wjr42",
        "reseller": "kaskldfhjl4",
        "location": "p28u348qwfn",
    },
}

mock_huntgroup_dialog_bundle = mock_callee_dialog_bundle

static_mock_dialog_params = {
    "user_id": "iufasdifj23",
    "account_id": "29ru-q9wjr42",
    "reseller_id": "kaskldfhjl4",
    "location_id": "p28u348qwfn",
    "peer_id": "fi234908r",
    "callee_ip": "192.111.135",
}


def make_key(name: str) -> str:
    """
    Create a counter's key value using the key_name:keu_uuid notation.

    :param name: The name of the key.
    :return: The full key.
    """
    key = difflib.get_close_matches(name, static_mock_dialog_params.keys(), 1, 0.42)
    if len(key) > 0:
        return f"{name}:{static_mock_dialog_params[key[0]]}"
    return name


def make_keys(*names: str) -> list[str]:
    """
    Create a list of counter keys.

    :param names: A list of key names.
    :return: A list containing the redis keys.
    """
    return list(map(make_key, names))


def assert_key_value(target, keys) -> None:
    """
    Assert the target value of a group of keys.

    :param target: The expected value for all keys.
    :param keys: A list of keys.
    :return:
    """
    for key in keys:
        assert RedisManager.get_central_value(key) == target


def test_initialize_call_counter_dialog_profile(fake_dialog_manager, fake_redis_manager) -> None:
    """
    Test initializing the ize_peer dialog profile.

    :param fake_dialog_manager: Mocked DialogManager class.
    :param fake_redis_manager: Mocked RedisManager class.
    :return:
    """
    response = client.post(f"{prefix}/counter", json=mock_call_counter_dialog_params)
    assert response.status_code == status.HTTP_200_OK
    keys = make_keys("user")
    assert_key_value(1, keys)
    assert RedisManager.get_local_value(mock_dialog_uuid) == [*keys]


def test_initialize_general_counter_dialog_profile(fake_dialog_manager, fake_redis_manager) -> None:
    """
    Test initializing the ize_peer dialog profile.

    :param fake_dialog_manager: Mocked DialogManager class.
    :param fake_redis_manager: Mocked RedisManager class.
    :return:
    """
    response = client.post(f"{prefix}/counter", json=mock_general_counter_dialog_params)
    assert response.status_code == status.HTTP_200_OK
    keys = make_keys("peer:faxserver")
    assert_key_value(1, keys)
    assert RedisManager.get_local_value(mock_dialog_uuid) == [*keys]


def test_fail_to_initialize_invalid_counter_dialog_profile(
    fake_dialog_manager, fake_redis_manager
) -> None:
    """
    Test initializing the ize_peer dialog profile.

    :param fake_dialog_manager: Mocked DialogManager class.
    :param fake_redis_manager: Mocked RedisManager class.
    :return:
    """
    response = client.post(f"{prefix}/counter", json=mock_invalid_counter_dialog_params)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"message": "counter unknown"}


def test_fail_to_initialize_call_counter_dialog_profile(
    fake_dialog_manager, fake_redis_manager
) -> None:
    """
    Test initializing the ize_peer dialog profile.

    :param fake_dialog_manager: Mocked DialogManager class.
    :param fake_redis_manager: Mocked RedisManager class.
    :return:
    """
    response = client.post(f"{prefix}/counter", json=mock_call_counter_dialog_params_no_id)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"message": "counter id must be specified"}


def test_initialize_peer_dialog_profile(fake_dialog_manager, fake_redis_manager) -> None:
    """
    Test initializing the ize_peer dialog profile.

    :param fake_dialog_manager: Mocked DialogManager class.
    :param fake_redis_manager: Mocked RedisManager class.
    :return:
    """
    res = client.post(f"{prefix}/peer", json=mock_peer_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    keys = make_keys("peer", "peerout", "relay")
    assert_key_value(1, keys)
    assert Counter(RedisManager.get_local_value(mock_dialog_uuid)) == Counter([*keys])


def test_initialize_caller_dialog_profile(fake_dialog_manager, fake_redis_manager) -> None:
    """
    Test initializing the caller dialog profile.

    :param fake_dialog_manager: Mocked DialogManager class.
    :param fake_redis_manager: Mocked RedisManager class.
    :return:
    """
    res = client.post(f"{prefix}/user/caller", json=mock_caller_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    keys = make_keys(
        "user",
        "account",
        "reseller",
        "location",
        "userout",
        "accountout",
        "resellerout",
        "locationout",
    )
    assert_key_value(1, keys)
    assert Counter(RedisManager.get_local_value(mock_dialog_uuid)) == Counter([*keys])


def test_initialize_callee_dialog_profile(fake_dialog_manager, fake_redis_manager) -> None:
    """
    Test initializing the callee dialog profile.

    :param fake_dialog_manager: Mocked DialogManager class.
    :param fake_redis_manager: Mocked RedisManager class.
    :return:
    """
    res = client.post(f"{prefix}/user/callee", json=mock_callee_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    keys = make_keys("location")
    assert_key_value(1, keys)
    assert Counter(RedisManager.get_local_value(mock_dialog_uuid)) == Counter([*keys])


def test_initialize_active_caller_dialog_profile(fake_dialog_manager, fake_redis_manager) -> None:
    """
    Test initializing the active caller dialog profile.

    :param fake_dialog_manager: Mocked DialogManager class.
    :param fake_redis_manager: Mocked RedisManager class.
    :return:
    """
    res = client.post(f"{prefix}/user/caller/active", json=mock_active_user_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    keys = make_keys("activeuser")
    assert_key_value(1, keys)
    assert Counter(RedisManager.get_local_value(mock_dialog_uuid)) == Counter([*keys])


def test_initialize_active_callee_dialog_profile(fake_dialog_manager, fake_redis_manager) -> None:
    """
    Test initializing the active callee dialog profile.

    :param fake_dialog_manager: Mocked DialogManager class.
    :param fake_redis_manager: Mocked RedisManager class.
    :return:
    """
    res = client.post(f"{prefix}/user/callee/active", json=mock_active_user_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    keys = make_keys("activeuser")
    assert_key_value(1, keys)
    assert Counter(RedisManager.get_local_value(mock_dialog_uuid)) == Counter([*keys])


def test_initialize_caller_totals_dialog_profile(fake_dialog_manager, fake_redis_manager) -> None:
    """
    Test initializing the caller totals dialog profile.

    :param fake_dialog_manager: Mocked DialogManager class.
    :param fake_redis_manager: Mocked RedisManager class.
    :return:
    """
    res = client.post(f"{prefix}/user/caller/totals", json=mock_caller_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    keys = make_keys(
        "total",
        "totaluser",
        "totalaccount",
        "totalreseller",
        "totallocation",
        "totaluserout",
        "totalaccountout",
        "totalresellerout",
        "totallocationout",
    )
    assert_key_value(1, keys)
    assert Counter(RedisManager.get_local_value(mock_dialog_uuid)) == Counter([*keys])


def test_initialize_callee_totals_dialog_profile(fake_dialog_manager, fake_redis_manager) -> None:
    """
    Test initializing the callee totals dialog profile.

    :param fake_dialog_manager: Mocked DialogManager class.
    :param fake_redis_manager: Mocked RedisManager class.
    :return:
    """
    res = client.post(f"{prefix}/user/callee/totals", json=mock_callee_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    keys = make_keys("location")
    assert_key_value(1, keys)
    assert Counter(RedisManager.get_local_value(mock_dialog_uuid)) == Counter([*keys])


def test_delete_dialog_profile(fake_dialog_manager, fake_redis_manager) -> None:
    """
    Test updating the dialog profile.

    :param fake_dialog_manager: Mocked. DialogManager class
    :param fake_redis_manager: Mocked .RedisManager class
    :return:
    """
    res = client.post(f"{prefix}/peer", json=mock_peer_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    res = client.put(f"{prefix}/delete", json=mock_dialog_bundle)
    assert res.status_code == status.HTTP_200_OK
    keys = make_keys("peer", "peerout", "relay")
    assert_key_value(0, keys)
    assert RedisManager.get_local_value(mock_dialog_uuid) == []


def test_delete_user_dialog_profile(fake_dialog_manager, fake_redis_manager) -> None:
    """
    Test updating the user dialog profile.

    :param fake_dialog_manager: Mocked DialogManager. class
    :param fake_redis_manager: Mocked RedisManager c.lass
    :return:
    """
    res = client.post(f"{prefix}/user/caller", json=mock_caller_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    res = client.post(f"{prefix}/user/caller/totals", json=mock_caller_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    res = client.put(f"{prefix}/delete/user", json=mock_user_dialog_bundle)
    assert res.status_code == status.HTTP_200_OK
    all_keys = make_keys(
        "user",
        "account",
        "reseller",
        "location",
        "userout",
        "accountout",
        "resellerout",
        "locationout",
        "total",
        "totaluser",
        "totalaccount",
        "totalreseller",
        "totallocation",
        "totaluserout",
        "totalaccountout",
        "totalresellerout",
        "totallocationout",
    )
    deleted_keys = make_keys("user", "userout", "totaluser", "totaluserout")
    assert_key_value(0, deleted_keys)
    assert Counter(RedisManager.get_local_value(mock_dialog_uuid)) == Counter(
        [*[key for key in all_keys if key not in deleted_keys]]
    )


def test_delete_account_dialog_profile(fake_dialog_manager, fake_redis_manager) -> None:
    """
    Test updating the account dialog profile.

    :param fake_dialog_manager: Mocked DialogManager class.
    :param fake_redis_manager: Mocked RedisManager class.
    :return:
    """
    res = client.post(f"{prefix}/user/caller", json=mock_caller_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    res = client.post(f"{prefix}/user/caller/totals", json=mock_caller_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    res = client.put(f"{prefix}/delete/account", json=mock_account_dialog_bundle)
    assert res.status_code == status.HTTP_200_OK
    all_keys = make_keys(
        "user",
        "account",
        "reseller",
        "location",
        "userout",
        "accountout",
        "resellerout",
        "locationout",
        "total",
        "totaluser",
        "totalaccount",
        "totalreseller",
        "totallocation",
        "totaluserout",
        "totalaccountout",
        "totalresellerout",
        "totallocationout",
    )
    deleted_keys = make_keys("account", "accountout", "totalaccount", "totalaccountout")
    assert_key_value(0, deleted_keys)
    assert Counter(RedisManager.get_local_value(mock_dialog_uuid)) == Counter(
        [*[key for key in all_keys if key not in deleted_keys]]
    )


def test_delete_reseller_dialog_profile(fake_dialog_manager, fake_redis_manager) -> None:
    """
    Test updating the reseller dialog profile.

    :param fake_dialog_manager: Mocked DialogManager class.
    :param fake_redis_manager: Mocked RedisManager class.
    :return:
    """
    res = client.post(f"{prefix}/user/caller", json=mock_caller_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    res = client.post(f"{prefix}/user/caller/totals", json=mock_caller_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    res = client.put(f"{prefix}/delete/reseller", json=mock_reseller_dialog_bundle)
    assert res.status_code == status.HTTP_200_OK
    all_keys = make_keys(
        "user",
        "account",
        "reseller",
        "location",
        "userout",
        "accountout",
        "resellerout",
        "locationout",
        "total",
        "totaluser",
        "totalaccount",
        "totalreseller",
        "totallocation",
        "totaluserout",
        "totalaccountout",
        "totalresellerout",
        "totallocationout",
    )
    deleted_keys = make_keys("reseller", "resellerout", "totalreseller", "totalresellerout")
    assert_key_value(0, deleted_keys)
    assert Counter(RedisManager.get_local_value(mock_dialog_uuid)) == Counter(
        [*[key for key in all_keys if key not in deleted_keys]]
    )


def test_delete_location_dialog_profile(fake_dialog_manager, fake_redis_manager) -> None:
    """
    Test updating the location dialog profile.

    :param fake_dialog_manager: Mocked DialogManager class.
    :param fake_redis_manager: Mocked RedisManager class.
    :return:
    """
    res = client.post(f"{prefix}/user/caller", json=mock_caller_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    res = client.post(f"{prefix}/user/caller/totals", json=mock_caller_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    res = client.put(f"{prefix}/delete/location", json=mock_location_dialog_bundle)
    assert res.status_code == status.HTTP_200_OK
    all_keys = make_keys(
        "user",
        "account",
        "reseller",
        "location",
        "userout",
        "accountout",
        "resellerout",
        "locationout",
        "total",
        "totaluser",
        "totalaccount",
        "totalreseller",
        "totallocation",
        "totaluserout",
        "totalaccountout",
        "totalresellerout",
        "totallocationout",
    )
    deleted_keys = make_keys("location", "locationout", "totallocation", "totallocationout")
    assert_key_value(0, deleted_keys)
    assert Counter(RedisManager.get_local_value(mock_dialog_uuid)) == Counter(
        [*[key for key in all_keys if key not in deleted_keys]]
    )


def test_delete_peer_dialog_profile(fake_dialog_manager, fake_redis_manager) -> None:
    """
    Test updating the peer dialog profile.

    :param fake_dialog_manager: Mocked DialogManager. class
    :param fake_redis_manager: Mocked RedisManager c.lass
    :return:
    """
    res = client.post(f"{prefix}/user/caller", json=mock_caller_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    res = client.post(f"{prefix}/user/caller/totals", json=mock_caller_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    res = client.put(f"{prefix}/delete/peer", json=mock_peer_dialog_bundle)
    assert res.status_code == status.HTTP_200_OK
    all_keys = make_keys(
        "user",
        "account",
        "reseller",
        "location",
        "userout",
        "accountout",
        "resellerout",
        "locationout",
        "total",
        "totaluser",
        "totalaccount",
        "totalreseller",
        "totallocation",
        "totaluserout",
        "totalaccountout",
        "totalresellerout",
        "totallocationout",
    )
    deleted_keys = make_keys("peer", "peerout", "relay")
    assert_key_value(0, deleted_keys)
    assert Counter(RedisManager.get_local_value(mock_dialog_uuid)) == Counter(
        [*[key for key in all_keys if key not in deleted_keys]]
    )


def test_delete_active_user_dialog_profile(fake_dialog_manager, fake_redis_manager) -> None:
    """
    Test updating the active user dialog profile.

    :param fake_dialog_manager: Mocked DialogManager class.
    :param fake_redis_manager: Mocked RedisManager class.
    :return:
    """
    res = client.post(f"{prefix}/user/caller/active", json=mock_active_user_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    res = client.put(f"{prefix}/delete/user/active", json=mock_user_dialog_bundle)
    assert res.status_code == status.HTTP_200_OK
    deleted_keys = make_keys("activeuser")
    assert_key_value(0, deleted_keys)
    assert RedisManager.get_local_value(mock_dialog_uuid) == []


def test_delete_transferred_callee_dialog_profile(fake_dialog_manager, fake_redis_manager) -> None:
    """
    Test updating the transferred callee dialog profile.

    :param fake_dialog_manager: Mocked DialogManager class.
    :param fake_redis_manager: Mocked RedisManager class.
    :return:
    """
    res = client.post(f"{prefix}/user/caller", json=mock_caller_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    res = client.post(f"{prefix}/user/caller/totals", json=mock_caller_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    res = client.put(f"{prefix}/delete/transferred/callee", json=mock_callee_dialog_bundle)
    assert res.status_code == status.HTTP_200_OK
    all_keys = make_keys(
        "user",
        "account",
        "reseller",
        "location",
        "userout",
        "accountout",
        "resellerout",
        "locationout",
        "total",
        "totaluser",
        "totalaccount",
        "totalreseller",
        "totallocation",
        "totaluserout",
        "totalaccountout",
        "totalresellerout",
        "totallocationout",
    )
    deleted_keys = make_keys(
        "user",
        "totaluser",
        "activeuser",
        "account",
        "totalaccount",
        "location",
        "totallocation",
        "general",
        "incoming",
        "total",
    )
    assert_key_value(0, deleted_keys)
    assert Counter(RedisManager.get_local_value(mock_dialog_uuid)) == Counter(
        [*[key for key in all_keys if key not in deleted_keys]]
    )


def test_delete_transferred_caller_dialog_profile(fake_dialog_manager, fake_redis_manager) -> None:
    """
    Test updating the transferred caller dialog profile.

    :param fake_dialog_manager: Mocked DialogManager class.
    :param fake_redis_manager: Mocked RedisManager class.
    :return:
    """
    res = client.post(f"{prefix}/user/caller", json=mock_caller_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    res = client.post(f"{prefix}/user/caller/totals", json=mock_caller_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    res = client.put(f"{prefix}/delete/transferred/caller", json=mock_caller_dialog_bundle)
    assert res.status_code == status.HTTP_200_OK
    all_keys = make_keys(
        "user",
        "account",
        "reseller",
        "location",
        "userout",
        "accountout",
        "resellerout",
        "locationout",
        "total",
        "totaluser",
        "totalaccount",
        "totalreseller",
        "totallocation",
        "totaluserout",
        "totalaccountout",
        "totalresellerout",
        "totallocationout",
    )
    deleted_keys = make_keys(
        "user",
        "userout",
        "totaluser",
        "totaluserout",
        "activeuser",
        "account",
        "accountout",
        "totalaccount",
        "totalaccountout",
        "location",
        "locationout",
        "reseller",
        "resellerout",
        "totalreseller",
        "totalresellerout",
        "general",
        "incoming",
        "total",
    )
    assert_key_value(0, deleted_keys)
    assert Counter(RedisManager.get_local_value(mock_dialog_uuid)) == Counter(
        [*[key for key in all_keys if key not in deleted_keys]]
    )


def test_delete_huntgroup_dialog_profile(fake_dialog_manager, fake_redis_manager) -> None:
    """
    Test updating the huntgroup dialog profile.

    :param fake_dialog_manager: Mocked DialogManager class.
    :param fake_redis_manager: Mocked RedisManager class.
    :return:
    """
    res = client.post(f"{prefix}/user/caller", json=mock_caller_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    res = client.post(f"{prefix}/user/caller/totals", json=mock_caller_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    res = client.put(f"{prefix}/delete/huntgroup", json=mock_huntgroup_dialog_bundle)
    assert res.status_code == status.HTTP_200_OK
    all_keys = make_keys(
        "user",
        "account",
        "reseller",
        "location",
        "userout",
        "accountout",
        "resellerout",
        "locationout",
        "total",
        "totaluser",
        "totalaccount",
        "totalreseller",
        "totallocation",
        "totaluserout",
        "totalaccountout",
        "totalresellerout",
        "totallocationout",
    )
    deleted_keys = make_keys(
        "user",
        "userout",
        "totaluser",
        "totaluserout",
        "activeuser",
        "account",
        "accountout",
        "totalaccount",
        "totalaccountout",
        "location",
        "locationout",
        "totallocation",
        "totallocationout",
        "general",
        "incoming",
        "total",
    )
    assert_key_value(0, deleted_keys)
    assert Counter(RedisManager.get_local_value(mock_dialog_uuid)) == Counter(
        [*[key for key in all_keys if key not in deleted_keys]]
    )


def test_get_counter(fake_redis_manager) -> None:
    """
    Test getter of counter.

    :param fake_redis_manager: Mocked RedisManager class.
    :return:
    """
    user_id = mock_caller_dialog_params["user_id"]
    url = f"/api/v1/counter/user:{user_id}"
    res = client.get(url)
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {"name": f"user:{user_id}", "value": 0}
    res = client.post(f"{prefix}/user/caller", json=mock_caller_dialog_params)
    assert res.status_code == status.HTTP_200_OK
    res = client.get(url)
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {"name": f"user:{user_id}", "value": 1}


def test_send_dialog_without_tags_when_required(fake_dialog_manager, fake_redis_manager) -> None:
    """
    Test initializing the callee dialog profile.

    :param fake_dialog_manager: Mocked DialogManager class.
    :param fake_redis_manager: Mocked RedisManager class.
    :return:
    """
    config.settings.use_dialog_id_tags = True
    response = client.post(f"{prefix}/user/caller/active", json=mock_no_tag_dialog_params)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"message": "Dialog id tags can't be empty"}
