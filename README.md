<br>
<table align="center">
  <tr>
    <td><img src="https://www.gitbook.com/cdn-cgi/image/width=40,dpr=2,height=40,fit=contain,format=auto/https%3A%2F%2F4183870952-files.gitbook.io%2F~%2Ffiles%2Fv0%2Fb%2Fgitbook-legacy-files%2Fo%2Fspaces%252F-MUp92Ia17fU7ZvnMCAm%252Favatar-1624571916925.png%3Fgeneration%3D1624571917228957%26alt%3Dmedia" alt="Pinata Logo" width="80"></td>
    <td><h1>Pinata Connection</h1></td>
  </tr>
</table>
<br>
This project is a user-friendly Streamlit application that provides an interactive interface for interacting with the Pinata IPFS API. It was developed as part of the Streamlit Connections Hackathon. The application is designed to make it easy for users to leverage the power of the InterPlanetary File System (IPFS) through Pinata's robust API, all within the convenience of Streamlit's interactive and user-friendly framework.
<br><br>
InterPlanetary File System (IPFS) is a protocol and network designed to create a content-addressable, peer-to-peer method of storing and sharing hypermedia in a distributed file system. Pinata is a platform that provides user-friendly IPFS infrastructure and makes it easy to interact with the IPFS network.
<br><br>

For more details on the Pinata API, you can check out their [official documentation](https://docs.pinata.cloud/pinata-api).
<br><br>
![Screenshot from 2023-07-22 21-28-41](https://github.com/BlurryFace04/Pinata-Connection/assets/64888928/3637138c-7079-4fe6-a99c-ae304f300ef3)

# Features
This application provides a wide range of features that allow users to interact with the Pinata API:
### 1. File Uploading:
Users can upload files directly to Pinata from their local system. The application provides a simple and intuitive interface for file selection and upload. Once the file is uploaded, the IPFS hash of the file is displayed, which can be used for future reference.

### 2. Pin by CID:
If users already have the Content Identifier (CID) of a file or dataset on IPFS, they can pin it directly using this feature. This is useful for ensuring the persistence of important data on the network.

### 3. Pin JSON:
Users can pin JSON objects directly to IPFS. This is a powerful feature for developers who want to store and share structured data.

### 4. Update Metadata:
Users can update the metadata of any pinned item. This includes the name of the pin and any key-value pairs associated with it. This feature provides flexibility in managing and organizing pinned data.

### 5. Unpin:
If a user no longer needs a file or dataset to persist on IPFS, they can unpin it using this feature. When you unpin something from an IPFS storage node, it is marked for garbage collection. When garbage collection runs, the content is permanently deleted from the storage node. 

### 6. Get Info:
Users can enter an IPFS hash to get detailed information about the corresponding pin by giving the ipfs_pin_hash as the input.

### 7. Query Data:
Users can query the data they have pinned based on different pin status, which are all, pinned and unpinned.

### 8. List by Jobs:
Users can list their data based on the job status of CIDs they have requested to be pinned to their account.

### 9. Data Usage:
Users can check their data usage on Pinata. This helps in keeping track of storage and understanding the distribution of data.

**Note on Directory Uploading Feature:** This application includes a feature for uploading directories to Pinata, which is designed to work on a local machine where the application has access to the file system. However, please be aware that this feature may not function as expected when the application is run in a cloud-based environment (like Streamlit Sharing), due to the application's limited access to the file system in such environments. If you're running this application on your local machine, you should be able to use the "Upload Directory" feature without any issues. In the [app.py](https://github.com/BlurryFace04/Pinata-Connection/blob/main/app.py) file, this feature is commented out. If you wish to use it, you can uncomment the relevant section in the app.py file when running the application locally.
<br><br>
All these features are presented in an interactive and user-friendly interface, making it easy for both technical and non-technical users to leverage the power of IPFS and Pinata.

# Usage
The application is hosted on Streamlit's community cloud and can be accessed [here](https://pinata.streamlit.app/).

The user interface is intuitive and easy to navigate. Each section of the application corresponds to a different feature of the Pinata API. Simply follow the prompts and enter the required information to use each feature.

# Contributing
Contributions to this project are welcome. If you have a feature request, bug report, or proposal for improvement, please open an issue on GitHub. If you want to contribute code, please fork the repository and submit a pull request.

# License
This project is licensed under the MIT License. See the [LICENSE file](https://github.com/BlurryFace04/Pinata-Connection/blob/main/LICENSE) for details.
