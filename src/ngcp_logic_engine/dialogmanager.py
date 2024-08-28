"""Dialog manager interface."""

from __future__ import annotations

from ngcp_logic_engine import config
from ngcp_logic_engine.models.dialog import (
    ActiveUserDialogParams,
    CalleeDialogParams,
    CallerDialogParams,
    Dialog,
    DialogIdBundle,
    DialogKeyIds,
    DialogKeys,
    PeerDialogParams,
)
from ngcp_logic_engine.redismanager import RedisManager


class DialogManager:
    """The DialogManager class orchestrates operations between the API and Redis."""

    @staticmethod
    def _parse_dialog_uuid(dialog: Dialog) -> str:
        """
        Construct dialog id.

        Parses the contents of a Dialog object to generate a unique id for
        the dialog.

        :param dialog: Dialog object containing the id parameters of the dialog.
        :return:
        """
        dialog_id: str = dialog.callid
        if config.settings.use_dialog_id_tags:
            dialog_id = f"{dialog.ftag}:{dialog.callid}:{dialog.ttag}"

        return dialog_id

    @classmethod
    def _set_dialog_profile_totals(cls, params: CallerDialogParams | CalleeDialogParams) -> None:
        """
        Set dialog profile totals.

        Creates the dialog profile counters, including totals, for the specified call identifier.

        :param params:
        :return:
        """
        dialog_uuid = cls._parse_dialog_uuid(params.dialog)

        if isinstance(params, CalleeDialogParams) and params.callee_ip:
            if params.location_id:
                cls._set_dialog_profile(dialog_uuid, "location", params.location_id)
            return

        cls._set_dialog_profile(dialog_uuid, "total")
        cls._set_dialog_profile(dialog_uuid, "totaluser", params.user_id)

        if not params.p_to_group or params.p_to_group != 1:
            cls._set_dialog_profile(dialog_uuid, "totalaccount", params.account_id)
            cls._set_dialog_profile(dialog_uuid, "totalreseller", params.reseller_id)

        if isinstance(params, CallerDialogParams):
            if params.location_id:
                cls._set_dialog_profile(dialog_uuid, "totallocation", params.location_id)
                cls._set_dialog_profile(dialog_uuid, "totallocationout", params.location_id)
            cls._set_dialog_profile(dialog_uuid, "totaluserout", params.user_id)
            if not params.p_to_group or params.p_to_group != 1:
                cls._set_dialog_profile(dialog_uuid, "totalaccountout", params.account_id)
                cls._set_dialog_profile(dialog_uuid, "totalresellerout", params.reseller_id)
        return

    @classmethod
    def _set_dialog_profile_user(cls, params: CallerDialogParams | CalleeDialogParams) -> None:
        """
        Set dialog profile for user.

        Creates the dialog profile counters for a user the specified call identifier.

        :param params:
        :return:
        """
        _type = "callee" if isinstance(params, CalleeDialogParams) else "caller"
        dialog_uuid = cls._parse_dialog_uuid(params.dialog)

        if isinstance(params, CalleeDialogParams) and params.callee_ip:
            if params.location_id:
                cls._set_dialog_profile(dialog_uuid, "location", params.location_id)
            return

        cls._set_dialog_profile(dialog_uuid, "user", params.user_id)

        if not params.p_to_group or params.p_to_group != 1:
            cls._set_dialog_profile(dialog_uuid, "account", params.account_id)
            cls._set_dialog_profile(dialog_uuid, "reseller", params.reseller_id)

        if isinstance(params, CallerDialogParams):
            if params.location_id:
                cls._set_dialog_profile(dialog_uuid, "location", params.location_id)
                cls._set_dialog_profile(dialog_uuid, "locationout", params.location_id)
            cls._set_dialog_profile(dialog_uuid, "userout", params.user_id)
            if not params.p_to_group or params.p_to_group != 1:
                cls._set_dialog_profile(dialog_uuid, "accountout", params.account_id)
                cls._set_dialog_profile(dialog_uuid, "resellerout", params.reseller_id)
        return

    @classmethod
    def _set_dialog_profile_active_user(cls, params: ActiveUserDialogParams) -> None:
        """
        Set dialog profile for active user.

        Creates the dialog profile counter for the active user for the specified call identifier.

        :param params:
        :return:
        """
        dialog_uuid = cls._parse_dialog_uuid(params.dialog)
        cls._set_dialog_profile(dialog_uuid, "activeuser", params.user_id)

    @classmethod
    def _set_dialog_profile(
        cls, dialog_uuid: str, dialog_key: str, dialog_key_id: str | None = None
    ) -> None:
        """
        Increase dialog profile counter for active user.

        Creates a counter if it doesn't exist and increases its value by 1.

        :param dialog_uuid:
        :param dialog_key:
        :param dialog_key_id:
        :return:
        """
        key = f"{dialog_key}:{dialog_key_id}" if dialog_key_id is not None else dialog_key
        RedisManager.create_key(dialog_uuid, key)

    @classmethod
    def set_dialog_profile_peer(cls, params: PeerDialogParams) -> None:
        """
        Set dialog profile for peer.

        Sets the dialog call-id and counters for a peer
        :param params:
        :return:
        """
        dialog_uuid = cls._parse_dialog_uuid(params.dialog)
        cls._set_dialog_profile(dialog_uuid, "peer", params.peer_id)
        cls._set_dialog_profile(dialog_uuid, "peerout", params.peer_id)
        cls._set_dialog_profile(dialog_uuid, "relay")

    @classmethod
    def set_dialog_profile_caller_totals(
        cls, params: CallerDialogParams | CalleeDialogParams
    ) -> None:
        """
        Set dialog profile totals for caller.

        Sets the dialog call-id and total counters for a caller.

        :param params:
        :return:
        """
        cls._set_dialog_profile_totals(params)

    @classmethod
    def set_dialog_profile_callee_totals(
        cls, params: CallerDialogParams | CalleeDialogParams
    ) -> None:
        """
        Set dialog profile totals for callee.

        Sets the dialog call-id and total counters for a callee.

        :param params:
        :return:
        """
        cls._set_dialog_profile_totals(params)

    @classmethod
    def set_dialog_profile_caller(cls, params: CallerDialogParams | CalleeDialogParams) -> None:
        """
        Set dialog profile for caller.

        Sets the dialog call-id and counters for a caller.

        :param params:
        :return:
        """
        cls._set_dialog_profile_user(params)

    @classmethod
    def set_dialog_profile_callee(cls, params: CallerDialogParams | CalleeDialogParams) -> None:
        """
        Set dialog profile for callee.

        Sets the dialog call-id and counters for a callee.

        :param params:
        :return:
        """
        cls._set_dialog_profile_user(params)

    @classmethod
    def set_dialog_profile_caller_active(cls, params: ActiveUserDialogParams) -> None:
        """
        Set dialog profile for active caller.

        Sets the dialog call-id and counters for an active caller.

        :param params:
        :return:
        """
        cls._set_dialog_profile_active_user(params)

    @classmethod
    def set_dialog_profile_callee_active(cls, params: ActiveUserDialogParams) -> None:
        """
        Set dialog profile for active callee.

        Sets the dialog call-id and counters for an active callee.
        :param params:
        :return:
        """
        cls._set_dialog_profile_active_user(params)

    @classmethod
    def _delete_dialog_key(
        cls, dialog_uuid: str, dialog_key: str, dialog_key_id: str | None
    ) -> None:
        """
        Remove key related to dialog profile counter.

        Removes a counter.

        :param dialog_uuid: The parsed id of the dialog.
        :param dialog_key: The name of the counter.
        :param dialog_key_id: The counter id.
        :return:
        """
        key = f"{dialog_key}:{dialog_key_id}" if dialog_key_id is not None else dialog_key
        RedisManager.delete_key(dialog_uuid, key)

    @classmethod
    def delete_dialog_profile(cls, dialog: Dialog) -> None:
        """
        Delete dialog profile.

        Removes the user profile for the specified call identifier.

        :param dialog: Dialog object containing the id parameters of the dialog.
        :return:
        """
        dialog_uuid = cls._parse_dialog_uuid(dialog)
        RedisManager.delete_dialog_id(dialog_uuid)

    @classmethod
    def delete_dialog_profile_user(cls, bundle: DialogIdBundle) -> None:
        """
        Delete user profile.

        Removes the user profile for the specified call identifier.

        :param bundle: A collection of dialog identifiers.
        :return:
        """
        dialog_uuid = cls._parse_dialog_uuid(bundle.dialog)
        dialog_key_ids = bundle.dialog_key_ids
        dialog_keys = DialogKeys(
            user=["user", "userout", "totaluser", "totaluserout"],
        )
        cls._delete_profile(dialog_uuid, dialog_keys, dialog_key_ids)

    @classmethod
    def delete_dialog_profile_account(cls, bundle: DialogIdBundle) -> None:
        """
        Delete account profile.

        Removes the account profile for the specified call identifier.

        :param bundle: An object containing a Dialog object and the dialog's key ids
        :return:
        """
        dialog_uuid = cls._parse_dialog_uuid(bundle.dialog)
        dialog_key_ids = bundle.dialog_key_ids
        dialog_keys = DialogKeys(
            account=["account", "accountout", "totalaccount", "totalaccountout"],
        )
        cls._delete_profile(dialog_uuid, dialog_keys, dialog_key_ids)

    @classmethod
    def delete_dialog_profile_reseller(cls, bundle: DialogIdBundle) -> None:
        """
        Delete reseller profile.

        Removes the reseller profile for the specified call identifier.

        :param bundle: An object containing a Dialog object and the dialog's key ids
        :return:
        """
        dialog_uuid = cls._parse_dialog_uuid(bundle.dialog)
        dialog_key_ids = bundle.dialog_key_ids
        dialog_keys = DialogKeys(
            reseller=["reseller", "resellerout", "totalreseller", "totalresellerout"],
        )
        cls._delete_profile(dialog_uuid, dialog_keys, dialog_key_ids)

    @classmethod
    def delete_dialog_profile_location(cls, bundle: DialogIdBundle) -> None:
        """
        Delete location profile.

        Removes the location profile for the specified call identifier.

        :param bundle: An object containing a Dialog object and the dialog's key ids
        :return:
        """
        dialog_uuid = cls._parse_dialog_uuid(bundle.dialog)
        dialog_key_ids = bundle.dialog_key_ids
        dialog_keys = DialogKeys(
            location=["location", "locationout", "totallocation", "totallocationout"],
        )
        cls._delete_profile(dialog_uuid, dialog_keys, dialog_key_ids)

    @classmethod
    def delete_dialog_profile_peer(cls, bundle: DialogIdBundle) -> None:
        """
        Delete profile for a peer.

        Removes the peer profile for the specified call identifier.

        :param bundle: An object containing a Dialog object and the dialog's key ids
        :return:
        """
        dialog_uuid = cls._parse_dialog_uuid(bundle.dialog)
        dialog_key_ids = bundle.dialog_key_ids
        dialog_keys = DialogKeys(
            peer=["peer", "peerout"],
            general=["relay"],
        )
        cls._delete_profile(dialog_uuid, dialog_keys, dialog_key_ids)

    @classmethod
    def delete_dialog_profile_active_user(cls, bundle: DialogIdBundle) -> None:
        """
        Delete profile for an active user.

        Removes the active user profile for the specified call identifier.

        :param bundle: An object containing a Dialog object and the dialog's key ids
        :return:
        """
        dialog_uuid = cls._parse_dialog_uuid(bundle.dialog)
        dialog_key_ids = bundle.dialog_key_ids
        dialog_keys = DialogKeys(
            user=["activeuser"],
        )
        cls._delete_profile(dialog_uuid, dialog_keys, dialog_key_ids)

    @classmethod
    def delete_dialog_profile_transferred_callee(cls, bundle: DialogIdBundle) -> None:
        """
        Delete profile for a transferred callee.

        Removes the transferred callee profile for the specified call identifier.

        :param bundle: An object containing a Dialog object and the dialog's key ids
        :return:
        """
        dialog_uuid = cls._parse_dialog_uuid(bundle.dialog)
        dialog_key_ids = bundle.dialog_key_ids
        dialog_keys = DialogKeys(
            user=["user", "totaluser", "activeuser"],
            account=["account", "totalaccount"],
            location=["location", "totallocation"],
            general=["local", "incoming", "total"],
        )

        cls._delete_profile(dialog_uuid, dialog_keys, dialog_key_ids)

    @classmethod
    def delete_dialog_profile_transferred_caller(cls, bundle: DialogIdBundle) -> None:
        """
        Delete profile for a transferred caller.

        Removes the transferred caller profile for the specified call identifier.

        :param bundle: An object containing a Dialog object and the dialog's key ids
        :return:
        """
        dialog_uuid = cls._parse_dialog_uuid(bundle.dialog)
        dialog_key_ids = bundle.dialog_key_ids
        dialog_keys = DialogKeys(
            user=["user", "userout", "totaluser", "totaluserout", "activeuser"],
            account=["account", "accountout", "totalaccount", "totalaccountout"],
            location=["location", "locationout"],
            reseller=["reseller", "resellerout", "totalreseller", "totalresellerout"],
            general=["local", "incoming", "total"],
        )

        cls._delete_profile(dialog_uuid, dialog_keys, dialog_key_ids)

    @classmethod
    def delete_dialog_profile_huntgroup_member(cls, bundle: DialogIdBundle) -> None:
        """
        Delete profile for hg_member.

        Removes the hg_member profile for the specified call identifier.

        :param bundle: An object containing a Dialog object and the dialog's key ids
        :return:
        """
        dialog_uuid = cls._parse_dialog_uuid(bundle.dialog)
        dialog_key_ids = bundle.dialog_key_ids
        dialog_keys = DialogKeys(
            user=["user", "userout", "totaluser", "totaluserout", "activeuser"],
            account=["account", "accountout", "totalaccount", "totalaccountout"],
            location=["location", "locationout", "totallocation", "totallocationout"],
            general=["local", "incoming", "total"],
        )

        cls._delete_profile(dialog_uuid, dialog_keys, dialog_key_ids)

    @classmethod
    def _delete_profile(
        cls, dialog_uuid: str, dialog_keys: DialogKeys, dialog_key_ids: DialogKeyIds
    ) -> None:
        """
        Delete dialog profile for all given keys.

        Iterates over a set of keys and performs key removal operations.

        :param dialog_uuid:
        :param dialog_keys:
        :param dialog_key_ids:
        :return:
        """
        _dialog_key_ids = dialog_key_ids.model_dump()
        _dialog_key_ids["general"] = None
        for key_group, keys in iter(dialog_keys):
            if keys is not None:
                for key in keys:
                    cls._delete_dialog_key(dialog_uuid, key, _dialog_key_ids[key_group])
