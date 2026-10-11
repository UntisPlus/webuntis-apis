#!/usr/bin/env python3
"""Example 04 - Mobile REST auth: password -> JWT.

Calls `/WebUntis/api/mobile/v2/<school>/authentication` and prints the JWT.

Usage:
    export UNTIS_SERVER=mese
    export UNTIS_SCHOOL=demo-school
    export UNTIS_USER=demo
    export UNTIS_PASSWORD=demo
    python3 examples/python/04_mobile_jwt.py

See docs/06-mobile-rest-auth.md. The token is what 05_view_rest.py expects in
the UNTIS_JWT variable.
"""

from lib import Session, jwt_exp, need, server_base


def main():
    school = need("UNTIS_SCHOOL")
    url = f"{server_base()}/WebUntis/api/mobile/v2/{school}/authentication"
    session = Session()
    status, data, _ = session.request(
        url,
        data={"username": need("UNTIS_USER"), "password": need("UNTIS_PASSWORD")},
    )
    print(f"# POST {url} -> HTTP {status}")

    if not isinstance(data, dict) or "jwt" not in data:
        print(data)
        return

    print(f"# jwt: {data['jwt'][:60]}...")
    print(f"# isPasswordChangeRequired={data.get('isPasswordChangeRequired')}")
    print(f"# isEmailUpdateRequired={data.get('isEmailUpdateRequired')}")
    exp = jwt_exp(data["jwt"])
    if exp:
        print(f"# exp={exp}")
    print()
    print("# next: export UNTIS_JWT=<jwt>   and run 05_view_rest.py")


if __name__ == "__main__":
    main()
