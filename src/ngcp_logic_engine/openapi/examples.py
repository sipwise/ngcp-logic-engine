"""Examples module."""

from types import SimpleNamespace
from typing import Any

_routes = {
    "get": {},
    "post": {
        "peer": {
            "payload": {
                "valid": {
                    "value": {
                        "dialog": {
                            "callid": "8fasnef81iu2jnfdojqwefhouf",
                            "ftag": "$12312312$",
                            "ttag": "$ttag232421$",
                        },
                        "peer_id": "fi234908r",
                    }
                }
            },
            "response": {},
        },
        "caller": {
            "payload": {
                "valid": {
                    "value": {
                        "dialog": {
                            "callid": "8fasnef81iu2jnfdojqwefhouf",
                            "ftag": "$12312312$",
                            "ttag": "$ttag232421$",
                        },
                        "p_to_group": 0,
                        "user_id": "iufasdifj23",
                        "account_id": "29ru-q9wjr42",
                        "reseller_id": "kaskldfhjl4",
                        "location_id": "p28u348qwfn",
                    }
                }
            },
            "response": {},
        },
        "callee": {
            "payload": {
                "valid": {
                    "value": {
                        "dialog": {
                            "callid": "8fasnef81iu2jnfdojqwefhouf",
                            "ftag": "$12312312$",
                            "ttag": "$ttag232421$",
                        },
                        "p_to_group": 0,
                        "user_id": "iufasdifj23",
                        "account_id": "29ru-q9wjr42",
                        "reseller_id": "kaskldfhjl4",
                        "location_id": "p28u348qwfn",
                        "callee_ip": "192.111.135",
                    }
                }
            },
            "response": {},
        },
        "activeuser": {
            "payload": {
                "valid": {
                    "value": {
                        "dialog": {
                            "callid": "8fasnef81iu2jnfdojqwefhouf",
                            "ftag": "$12312312$",
                            "ttag": "$ttag232421$",
                        },
                        "user_id": "iufasdifj23",
                    }
                }
            },
            "response": {},
        },
    },
    "put": {
        "delete": {
            "payload": {
                "valid": {
                    "value": {
                        "dialog": {
                            "callid": "8fasnef81iu2jnfdojqwefhouf",
                            "ftag": "$12312312$",
                            "ttag": "$ttag232421$",
                        },
                    }
                }
            },
            "response": {},
        },
        "user": {
            "payload": {
                "valid": {
                    "value": {
                        "dialog": {
                            "callid": "8fasnef81iu2jnfdojqwefhouf",
                            "ftag": "$12312312$",
                            "ttag": "$ttag232421$",
                        },
                        "dialog_key_ids": {
                            "user": "iufasdifj23",
                        },
                    },
                },
            },
            "response": {},
        },
        "account": {
            "payload": {
                "valid": {
                    "value": {
                        "dialog": {
                            "callid": "8fasnef81iu2jnfdojqwefhouf",
                            "ftag": "$12312312$",
                            "ttag": "$ttag232421$",
                        },
                        "dialog_key_ids": {
                            "account": "29ru-q9wjr42",
                        },
                    },
                },
            },
            "response": {},
        },
        "location": {
            "payload": {
                "valid": {
                    "value": {
                        "dialog": {
                            "callid": "8fasnef81iu2jnfdojqwefhouf",
                            "ftag": "$12312312$",
                            "ttag": "$ttag232421$",
                        },
                        "dialog_key_ids": {
                            "location": "p28u348qwfn",
                        },
                    },
                },
            },
            "response": {},
        },
        "reseller": {
            "payload": {
                "valid": {
                    "value": {
                        "dialog": {
                            "callid": "8fasnef81iu2jnfdojqwefhouf",
                            "ftag": "$12312312$",
                            "ttag": "$ttag232421$",
                        },
                        "dialog_key_ids": {
                            "reseller": "kaskldfhjl4",
                        },
                    },
                },
            },
            "response": {},
        },
        "peer": {
            "payload": {
                "valid": {
                    "value": {
                        "dialog": {
                            "callid": "8fasnef81iu2jnfdojqwefhouf",
                            "ftag": "$12312312$",
                            "ttag": "$ttag232421$",
                        },
                        "dialog_key_ids": {
                            "peer": "fi234908r",
                        },
                    },
                },
            },
            "response": {},
        },
        "callee": {
            "payload": {
                "valid": {
                    "value": {
                        "dialog": {
                            "callid": "8fasnef81iu2jnfdojqwefhouf",
                            "ftag": "$12312312$",
                            "ttag": "$ttag232421$",
                        },
                        "dialog_key_ids": {
                            "user": "iufasdifj23",
                            "account": "29ru-q9wjr42",
                            "location": "p28u348qwfn",
                        },
                    },
                },
            },
            "response": {},
        },
        "caller": {
            "payload": {
                "valid": {
                    "value": {
                        "dialog": {
                            "callid": "8fasnef81iu2jnfdojqwefhouf",
                            "ftag": "$12312312$",
                            "ttag": "$ttag232421$",
                        },
                        "dialog_key_ids": {
                            "user": "iufasdifj23",
                            "account": "29ru-q9wjr42",
                            "location": "p28u348qwfn",
                            "reseller": "kaskldfhjl4",
                        },
                    },
                },
            },
            "response": {},
        },
        "huntgroup": {
            "payload": {
                "valid": {
                    "value": {
                        "dialog": {
                            "callid": "8fasnef81iu2jnfdojqwefhouf",
                            "ftag": "$12312312$",
                            "ttag": "$ttag232421$",
                        },
                        "dialog_key_ids": {
                            "user": "iufasdifj23",
                            "account": "29ru-q9wjr42",
                            "location": "p28u348qwfn",
                        },
                    },
                },
            },
            "response": {},
        },
    },
}

model = {
    "name": {
        "payload": {
            "valid": {
                "value": {
                    "dialog": {
                        "callid": "8fasnef81iu2jnfdojqwefhouf",
                        "ftag": "$12312312$",
                        "ttag": "$ttag232421$",
                    },
                    "dialog_key_ids": {
                        "user": "iufasdifj23",
                    },
                },
            },
        },
        "response": {},
    }
}


class NestedNamespace(SimpleNamespace):
    """Allows use of dot notation for namespace attributes."""

    def __init__(self, dictionary: dict[str, Any], **kwargs: str) -> None:
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, NestedNamespace(value))
            else:
                self.__setattr__(key, value)


routes = NestedNamespace(_routes)
