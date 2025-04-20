def article_exists(doi):
    """
    Dummy function to simulate checking for article existence.
    Always returns True.
    """
    return True

def download_xml(doi):
    """
    Dummy function to simulate downloading an XML file for the given DOI.
    Creates a dummy XML file in the app/system_data directory.
    """
    import os
    xml_filename = f"{doi.replace('/', '_')}_dummy.xml"
    xml_dir = os.path.join("app", "system_data")
    if not os.path.exists(xml_dir):
        os.makedirs(xml_dir)
    xml_path = os.path.join(xml_dir, xml_filename)
    with open(xml_path, "w") as f:
        f.write(f"<xml><doi>{doi}</doi><content>Dummy content for DOI {doi}</content></xml>")
    return xml_path
