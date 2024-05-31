from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    import ovh
    from ovh.exceptions import APIError     # type: ignore
    HAS_OVH = True
except ImportError:
    HAS_OVH = False


# Build and Return OVH Client from Module Informations
def ovh_client(module):

    # If OVH Lib is not loaded
    if not HAS_OVH:

        # Fail Message
        module.fail_json(msg='Python module python-ovh is required')

    # Required Module Keys
    credential_keys = [
        'endpoint',
        'application_key',
        'application_secret',
        'consumer_key'
    ]

    # Match Required Keys with Mocule Parameters
    # Find each credential_keys entry in module.params (Build Boolean array)
    credential_parameters = [cred_key in module.params for cred_key in credential_keys]

    try:

        # If All Credentials keyx are present in Module Parameters
        if all(credential_parameters):

            # Build OVH Client from Module Parameters
            client = ovh.Client(**{credential: module.params[credential] for credential in credential_keys})

        else:

            # Build Default OVH Client
            client = ovh.Client()

    except APIError as api_error:

        # Error Message for Mocule
        module.fail_json(msg="Failed to build OVH API Client: {0}".format(api_error))

    # Return Client
    return client
