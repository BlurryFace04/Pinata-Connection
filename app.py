import streamlit as st
from pinata_connection import PinataConnection
import json

# Set page title and icon
st.set_page_config(page_title="Pinata Connection", page_icon="https://www.gitbook.com/cdn-cgi/image/width=40,dpr=2,height=40,fit=contain,format=auto/https%3A%2F%2F4183870952-files.gitbook.io%2F~%2Ffiles%2Fv0%2Fb%2Fgitbook-legacy-files%2Fo%2Fspaces%252F-MUp92Ia17fU7ZvnMCAm%252Favatar-1624571916925.png%3Fgeneration%3D1624571917228957%26alt%3Dmedia")

# Initialize the connection
conn = st.experimental_connection('pinata', type=PinataConnection)

# Display a title
col1, col2, col3, col4 = st.columns([1.5, 1, 5, 1.5])
col2.image('https://www.gitbook.com/cdn-cgi/image/width=40,dpr=2,height=40,fit=contain,format=auto/https%3A%2F%2F4183870952-files.gitbook.io%2F~%2Ffiles%2Fv0%2Fb%2Fgitbook-legacy-files%2Fo%2Fspaces%252F-MUp92Ia17fU7ZvnMCAm%252Favatar-1624571916925.png%3Fgeneration%3D1624571917228957%26alt%3Dmedia', width=80)
col3.title("Pinata Connection")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# File uploader
st.subheader("1. Upload File")
file_path = st.file_uploader("Upload a file")

if file_path is not None and st.button("Upload File", key="upload_file"):
    # Upload the file
    upload_response = conn.upload_file(file_path)
    st.session_state['upload_response'] = upload_response

if 'upload_response' in st.session_state:
    st.write(st.session_state['upload_response'])

    # Unpin button
    if st.button("Unpin this file", key="unpin_file"):
        ipfs_hash = st.session_state['upload_response']['IpfsHash']
        unpin_response = conn.unpin(ipfs_hash)
        st.write(unpin_response)

# Directory uploader: UNCOMMENT THIS SECTION IN A LOCAL SYSTEM
# st.subheader("Upload Directory")
# directory_path = st.text_input("Enter the absolute path of a directory")

# if directory_path and st.button("Upload Directory", key="upload_directory"):
#     # Upload the directory
#     upload_response = conn.upload_directory(directory_path)
#     st.session_state['directory_upload_response'] = upload_response

# if 'directory_upload_response' in st.session_state:
#     st.write(st.session_state['directory_upload_response'])

#     # Unpin button
#     if st.button("Unpin this directory", key="unpin_directory"):
#         ipfs_hash = st.session_state['directory_upload_response']['IpfsHash']
#         unpin_response = conn.unpin(ipfs_hash)
#         st.write(unpin_response)

# Pin by CID
st.subheader("2. Pin by CID")
with st.expander("Options"):
    cid_input = st.text_input("Enter a CID to pin")
    name_input = st.text_input("Enter a name for the pin")

    if cid_input and name_input and st.button("Pin by CID", key="pin_cid"):
        cid_response = conn.pin_by_cid(cid_input, name_input)
        st.session_state['cid_response'] = cid_response

if 'cid_response' in st.session_state:
    st.write(st.session_state['cid_response'])

    # Unpin button
    if st.button("Unpin this file", key="unpin_cid"):
        ipfs_hash = st.session_state['cid_response']['IpfsHash']
        unpin_response = conn.unpin(ipfs_hash)
        st.write(unpin_response)

# Pin JSON
st.subheader("3. Pin JSON")
with st.expander("Options"):
    json_content_input = st.text_input("Enter JSON content to pin (as a JSON string)")
    json_name_input = st.text_input("Enter a name for the JSON pin")

    if json_content_input and json_name_input and st.button("Pin JSON", key="pin_json"):
        try:
            json_content = json.loads(json_content_input)
            json_response = conn.pin_by_json(json_content, json_name_input)
            st.session_state['json_response'] = json_response

        except json.decoder.JSONDecodeError:
            st.error("Invalid JSON string")

if 'json_response' in st.session_state:
    st.write(st.session_state['json_response'])

    # Unpin button
    if st.button("Unpin this file", key="unpin_json"):
        ipfs_hash = st.session_state['json_response']['IpfsHash']
        unpin_response = conn.unpin(ipfs_hash)
        st.write(unpin_response)

# Update metadata
st.subheader("4. Update Metadata")
with st.expander("Options"):
    ipfs_hash_input = st.text_input("Enter an IPFS hash to update its metadata")
    name_input = st.text_input("Enter a new name for the pin")

    num_key_value_pairs = st.number_input("Number of key-value pairs", min_value=0, max_value=10, value=0)

    keyvalues = {}
    for i in range(num_key_value_pairs):
        columns = st.columns(2)
        key = columns[0].text_input(f"Enter key {i + 1}")
        value = columns[1].text_input(f"Enter value {i + 1}")
        if key and value:
            keyvalues[key] = value

    if ipfs_hash_input and (name_input or keyvalues) and st.button("Update Metadata", key="update_metadata"):
        if keyvalues is not {}:
            update_metadata_response = conn.update_metadata(ipfs_hash_input, name_input, keyvalues)
        else:
            update_metadata_response = conn.update_metadata(ipfs_hash_input, name_input)
        st.session_state['update_metadata_response'] = update_metadata_response

if 'update_metadata_response' in st.session_state:
    st.write(st.session_state['update_metadata_response'])

# Unpin
st.subheader("5. Unpin")
unpin_hash_input = st.text_input("Enter an IPFS hash to unpin")
if unpin_hash_input and st.button("Unpin", key="unpin"):
    unpin_response = conn.unpin(unpin_hash_input)
    st.session_state['unpin_response'] = unpin_response

if 'unpin_response' in st.session_state:
    st.write(st.session_state['unpin_response'])

# Get with a specific hash
st.subheader("6. Get Info")
hash_input = st.text_input("Enter an IPFS hash to get its info")
if hash_input and st.button("Get Info", key="get_info"):
    hash_response = conn.query(hash_contains=hash_input, ttl=0)
    st.session_state['hash_response'] = hash_response

if 'hash_response' in st.session_state:
    st.write(st.session_state['hash_response'])

# Get with a specific status
st.subheader("7. Query Data")
status_options = [None, "all", "pinned", "unpinned"]
status = st.selectbox("Select pin status to query the data", status_options)

if status and st.button("Query Data", key="query_data"):
    pins_response = conn.query(status=status, ttl=0)
    st.session_state['pins_response'] = pins_response

if 'pins_response' in st.session_state and status is not None:
    st.write(st.session_state['pins_response'])

if status is None:
    st.session_state.pop('pins_response', None)

# List by jobs
st.subheader("8. List by Jobs")
jobs_options = [None, "prechecking", "searching", "retrieving", "expired", "over_free_limit", "over_max_size",
                "invalid_object", "bad_host_node"]
jobs = st.selectbox("Select job status to list the data", jobs_options)

if jobs and st.button("List by Jobs", key="list_jobs"):
    jobs_response = conn.list_by_jobs(status=jobs, ttl=0)
    st.session_state['jobs_response'] = jobs_response

if 'jobs_response' in st.session_state and jobs is not None:
    st.write(st.session_state['jobs_response'])

if jobs is None:
    st.session_state.pop('jobs_response', None)

# Get data usage
st.subheader("9. Data Usage")
if st.button("Get data usage", key="data_usage"):
    usage_response = conn.data_usage()
    st.session_state['usage_response'] = usage_response

if 'usage_response' in st.session_state:
    st.write(st.session_state['usage_response'])

st.markdown("---")
st.markdown("Made with :heart: by Blurry Face")
