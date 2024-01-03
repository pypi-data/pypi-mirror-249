from fabric_cm.credmgr.credmgr_proxy import CredmgrProxy

if __name__ == '__main__':
    cm = CredmgrProxy(credmgr_host="alpha-2.fabric-testbed.net", cookie_name="fabric-service-alpha")
    # By default; opens Chrome
    status, tokens = cm.create(project_name="CF TEST", comment="Create via Chrome")
    print(f"Token generated via Chrome: {tokens}")

    # By default; opens Chrome
    status, tokens = cm.create(project_name="CF TEST", browser_name="firefox", comment="Create via Firefox")
    print(f"Token generated via Firefox: {tokens}")

    # By default; opens Chrome
    status, tokens = cm.create(project_name="CF TEST", browser_name="safari", comment="Create via Safari")
    print(f"Token generated via Safari: {tokens}")



