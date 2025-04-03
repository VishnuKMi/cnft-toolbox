# Compressed NFT processing

## Introduction

Compressed NFT (cNFT) is a specialized digital asset format that optimizes data storage. Data compression algorithms reduce file sizes while preserving each asset’s uniqueness. This process saves server space and lowers data storage and transmission costs. In addition, Merkle trees minimize storage requirements and enhance the efficiency of cNFT collections.

## Features

- **Resource savings**: Merkle trees store only essential data, reducing gas costs and network load.
- **Improved scalability**: Efficient contracts can handle large NFT volumes without performance loss.
- **Optimized data storage**: Keeping minimal on-chain information boosts system responsiveness and saves space.
- **Enhanced security**: Merkle trees enable fast data integrity checks and robust asset protection.
- **Cost reduction**: Shift minting costs to end users and create “virtual” on-chain items only when needed.

## Supporting compressed NFT in wallets and marketplaces

**Current limitations**  
Most popular wallets and marketplaces do not display unclaimed cNFTs or NFTs from collections that are not official partners. For example, the Telegram wallet and the Getgems marketplace index only the first 200 items for unofficial collections, which poses challenges for larger collections.

**Attack scenario**  
A malicious actor could create hundreds of thousands of NFTs at minimal cost, forcing marketplaces to store all related data—even if the attacker does not host the items but generates them on demand.

**Potential solution**  
Provide a dedicated interface where users can claim their cNFTs. Once claimed, NFTs are indexed and displayed in wallets and marketplaces as standard NFTs, ensuring better visibility and accessibility.

## Configuration and deployment guide

### NFT collection and item preparation

Before deployment, you need to prepare the metadata and images for your NFTs.

#### Metadata preparation

- **Collection metadata**  
  Create a `collection.json` file that includes the required fields as specified in the [NFT token data standard](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md#nft-collection-metadata-example-offchain).  
  **Example:**

  ```json
  {
    "name": "<collection name>",
    "description": "<collection description>",
    "image": "<link to the image (e.g. https://yourdomain.com/logo.png)>"
  }
  ```

* **NFT item metadata**  
   For each NFT, create a separate JSON file (e.g., `0.json`, `1.json`, etc.) with the required fields as specified in the [NFT token data standard](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md#nft-item-metadata-example-offchain).  
   **Example:**
  ```json
  {
    "name": "<item name>",
    "description": "<item description>",
    "image": "<link to the image (e.g. https://yourdomain.com/0.png)>"
  }
  ```

#### Resource preparation

- **Images**: Prepare images for the collection (for example, `logo.png` for the avatar) and for each NFT (for example, `0.png`, `1.png`, etc.).
- **JSON files**: Host your `collection.json` and NFT JSON files on a publicly accessible server or repository. Ensure each file has a unique URL.

> **Note:** All images and JSON files must be directly accessible via their URLs.

### TON Connect manifest preparation

Create a [TON Connect manifest](https://github.com/ton-blockchain/ton-connect/blob/main/requests-responses.md#app-manifest) JSON file to describe your application during the wallet connection process.  
**Example:**

```json
{
  "url": "<app url>",
  "name": "<app name>",
  "iconUrl": "<app icon url>"
}
```

> **Note:** Ensure that this file is publicly accessible via its URL.

### Owner list preparation

Prepare an `owners.txt` file that lists the addresses of NFT owners, one per line. The first address corresponds to item index `0`, the second to item index `1`, and so on.  
**Example:**

```text
UQDYzZmfsrGzhObKJUw4gzdeIxEai3jAFbiGKGwxvxHinf4K
UQCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxZR0
```

### Infrastructure preparation

Set up a server to host your API and the interface for claiming NFTs. Also, obtain a domain for accessing the API. In this example, a local test deployment is run on a home machine using ngrok to create a public URL.

### Claiming API and interface setup

1.  **Clone the repository**  
    Clone the project containing all necessary source files:

    ```bash
    git clone https://github.com/nessshon/cnft-toolbox
    ```

2.  **Install dependencies**  
    Install Docker, Docker Compose, and ngrok, and ensure they are properly configured on your machine.
3.  **Create a Telegram bot**  
    Create a Telegram bot and obtain its API token.
4.  **Expose your API**  
    Use ngrok to create a public URL for testing:

    ```bash
    ngrok http 8080
    ```

    **For production:** Set up a custom domain and configure Nginx to proxy requests to your API on port 8080. This involves:

    - Registering a domain and pointing it to your server.
    - Configuring Nginx to proxy requests to your API on port 8080.

5.  **Create a `.env` file**  
    Duplicate the `env.example` file to `.env` and update it with your specific configuration. The table below describes each key:

    | **Key**                   | **Description**                                                                 | **Example**                                      | **Notes**                                          |
    | ------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------ | -------------------------------------------------- |
    | `PORT`                    | Port on which the API will run.                                                 | `8080`                                           |                                                    |
    | `ADMIN_USERNAME`          | Admin username for accessing restricted functionalities.                        | `admin`                                          |                                                    |
    | `ADMIN_PASSWORD`          | Admin password for accessing restricted functionalities.                        | `password`                                       |                                                    |
    | `DEPTH`                   | Depth for the NFT collection (max items = `2^DEPTH`; maximum DEPTH is 30).      | `20`                                             |                                                    |
    | `IS_TESTNET`              | Specify if you are connecting to the TON testnet (`true`) or mainnet (`false`). | `true` or `false`                                |                                                    |
    | `POSTGRES_PASSWORD`       | Password for PostgreSQL authentication.                                         | `secret`                                         |                                                    |
    | `POSTGRES_DB`             | Name of the PostgreSQL database.                                                | `merkleapi`                                      |                                                    |
    | `POSTGRES_URI`            | Full connection URI for PostgreSQL.                                             | `postgresql://postgres:secret@db:5432/merkleapi` |                                                    |
    | `BOT_TOKEN`               | Token for your Telegram bot (from [@BotFather](https://t.me/BotFather)).        | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`      | Used for the NFT claiming interface.               |
    | `API_BASE_URL`            | External domain of your API.                                                    | `https://example.ngrok.io`                       | Replace with your public URL (e.g., via ngrok).    |
    | `TONCONNECT_MANIFEST_URL` | URL for the TON Connect manifest file.                                          | `https://example.com/tonconnect-manifest.json`   | Replace with the public URL of your manifest file. |
    | `COLLECTION_ADDRESS`      | Address of the NFT collection.                                                  |                                                  | Fill this in **after** deploying the collection.   |

6.  **Start the API and database**  
    Run the following command to start the API and database:

    ```bash
    docker-compose up -d db api
    ```

7.  **Migrate the database**  
    Create the required tables in the database:

    ```bash
    docker-compose exec api /ctl migrate
    ```

8.  **Add owners**  
    Place your `owners.txt` file (containing owner addresses) into the `api` folder, then run:

    ```bash
    docker-compose exec api /ctl add /api/owners.txt
    ```

9.  **Rediscover items**  
    In your browser, navigate to `<API_URI>/admin/rediscover` and log in using your `ADMIN_USERNAME` and `ADMIN_PASSWORD`. If successful, you will see `ok` in the browser. After a short time (depending on the number of items), a file (e.g., `1.json`) appears in the `api/apidata/upd` folder.
10. **Generate an update**  
    Run the following command to generate an update:

    ```bash
    docker-compose exec api /ctl genupd <path-to-update-file> <collection-owner> <collection-meta> <item-meta-prefix> <royalty-base> <royalty-factor> <royalty-recipient> <api-uri-including-v1>
    ```

    Replace the placeholders as follows:

    - **`<path-to-update-file>`**: Path to the update file created in step 9 (e.g., `api/apidata/upd/1.json`).
    - **`<collection-owner>`**: Address of the NFT collection owner.
    - **`<collection-meta>`**: Full URL to the collection metadata file (e.g., `https://yourdomain.com/collection.json`).
    - **`<item-meta-prefix>`**: Common prefix for item metadata (for example, if item 0 has metadata at `https://yourdomain.com/0.json`, use `https://yourdomain.com/`).
    - **`<royalty-base>`**: Numerator for royalties (for example, `10` for 10% if royalty-factor is 100).
    - **`<royalty-factor>`**: Denominator for royalties (for example, `100`).
    - **`<royalty-recipient>`**: Address receiving royalties (this can be the same as `<collection-owner>`).
    - **`<api-uri-including-v1>`**: Public API URL with the `/v1` postfix (for example, if you used `https://yourapi.com/admin/rediscover` to generate the update file, use `https://yourapi.com/v1` here).

11. **Invoke the `ton://` deeplink**  
    After generating the update, a `ton://` link appears in the console logs. Follow the link and confirm the transaction. For convenience, you can paste the link into a QR code generator and scan the QR code with the Tonhub wallet (on testnet or mainnet).
12. **Set the collection address**  
    In your browser, navigate to `<API_URI>/admin/setaddr/<collection-address>`, replacing `<collection-address>` with the address observed during the deployment step.
13. **Wait for confirmation**  
    Monitor the container API logs until you see a message indicating a `committed state`.

    ```bash
    docker-compose logs api
    ```

14. **Deployment complete!**

### Run the Telegram bot for NFT claiming interface

1.  **Update the `.env` file**  
    Add the `COLLECTION_ADDRESS` obtained during deployment to your `.env` file.
2.  **Start the Telegram bot**  
    Run the following command to start the bot:

    ```bash
    docker-compose up -d redis bot
    ```

3.  **Interact with the bot**  
    Open Telegram, navigate to your bot, and follow its instructions to claim NFTs or perform other actions.
4.  **Done!**

### Updating owners

Follow these steps to update the list of owners and integrate the changes into your NFT collection:

1.  **Prepare the new owners file**  
    Create a `new-owners.txt` file with the new owner addresses and place it in the `api` folder.
2.  **Add new owners**  
    Run:

    ```bash
    docker-compose exec api /ctl add /api/new-owners.txt
    ```

3.  **Rediscover items**  
    In your browser, navigate to `<API_URI>/admin/rediscover` and log in with your `ADMIN_USERNAME` and `ADMIN_PASSWORD`.
4.  **Locate the update file**  
    After rediscovering, locate the new update file in the `api/apidata/upd` folder (for example, `2.json` if the previous update was `1.json`).
5.  **Generate an update**  
    Run:

    ```bash
    docker-compose exec api /ctl genupd <path-to-update-file> <collection-address>
    ```

    Replace `<path-to-update-file>` with the new update file’s path (e.g., `api/apidata/upd/2.json`) and `<collection-address>` with the NFT collection address.

6.  **Invoke the `ton://` deeplink**  
    Follow the generated `ton://` link and confirm the transaction. You may also generate a QR code from the link and scan it with the Tonhub wallet.
7.  **Wait for confirmation**  
    Monitor the container API logs until you see a message indicating a `committed state`.

    ```bash
    docker-compose logs api
    ```

8.  **Done!**

## Conclusion

The Compressed NFT standard transforms the creation and management of NFT collections by offering a scalable, cost-effective solution for mass NFT production. By addressing the limitations of existing standards, this approach paves the way for broader adoption and innovative applications of NFT technology in community building and marketing campaigns.

## See also

- [Understanding compressed NFT on the TON blockchain](https://ambiguous-mandrill-06a.notion.site/Understanding-compressed-NFT-on-the-TON-blockchain-753ffbcbd1684aef963b5cfb6db93e55)
- [Compressed NFT standard implementation](https://github.com/ton-community/compressed-nft-contract)
- [Reference augmenting API implementation](https://github.com/ton-community/compressed-nft-api)
- [NFT collection metadata example](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md#nft-collection-metadata-example-offchain)
- [NFT item metadata example](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md#nft-item-metadata-example-offchain)
- [Compressed NFT toolbox](https://github.com/nessshon/cnft-toolbox)

update command : docker-compose exec api /ctl genupd api/apidata/upd/2.json 0QCD8mUrn1mjmWmzBGwhE0hisdaZ_mskYbxAGUGRuZoTSUgg https://ivory-holy-aardwolf-123.mypinata.cloud/ipfs/bafybeibfsfvt6i75sjlpzfujlgyylnwgyig3uuajlg5bc3pqzzvcdmrjhy/collection.json https://ivory-holy-aardwolf-123.mypinata.cloud/ipfs/bafybeibfsfvt6i75sjlpzfujlgyylnwgyig3uuajlg5bc3pqzzvcdmrjhy/ 10 100 0QCD8mUrn1mjmWmzBGwhE0hisdaZ_mskYbxAGUGRuZoTSUgg https://cf7f-103-153-105-135.ngrok-free.app/v1

ton://transfer/EQDCO7D7Pse83v1Hpr3nxs-NLVgveKqPAtwG3xHgHNRYqNMs?amount=50000000&init=te6cckECPAEABiUAAgE0AQIBFP8A9KQT9LzyyAsDBIUD9bC65ANCydl6mR-olHRGtn_p4IdvEEHrKINY9IVyFRSAEH5MpXPrNHMtNmCNhCJpDFY60z_NZIw3iAMoMjczQmkwBAUGBwIBYggJART_APSkE_S88sgLCgIACwwASwAKAGSAEH5MpXPrNHMtNmCNhCJpDFY60z_NZIw3iAMoMjczQmkwAQIBDQICzA4PAgEgEBECAWISEwH-AWh0dHBzOi8vaXZvcnktaG9seS1hYXJkd29sZi0xMjMubXlwaW5hdGEuY2xvdWQvaXBmcy9iYWZ5YmVpYmZzZnZ0Nmk3NXNqbHB6ZnVqbGd5eWxud2d5aWczdXVhamxnNWJjM3Bxenp2Y2RtcmpoeS9jb2xsZWN0aW9uLmpzbxQA4Gh0dHBzOi8vaXZvcnktaG9seS1hYXJkd29sZi0xMjMubXlwaW5hdGEuY2xvdWQvaXBmcy9iYWZ5YmVpYmZzZnZ0Nmk3NXNqbHB6ZnVqbGd5eWxud2d5aWczdXVhamxnNWJjM3Bxenp2Y2RtcmpoeS8AWmh0dHBzOi8vN2U5YS0xMDMtMTc5LTE5Ni0xMC5uZ3Jvay1mcmVlLmFwcC92MQIBIBUWAgEgFxgCASAZGgIBSBscAgLOHR4ACaEfn-AFAAJuAgEgHyACASAhIgIBICMkAFXTeAODfGOEt8IVKpCFzNrjfAkHgCCTfGANJ0GHwheAX8IIldeXAy_DD4AcAC24tdMfAC-EXQ1DHUMNBxyMsHAc8WzMmAIBICUmABu2C34AXwi6D-A6hh8IkAANtQ2eAF8IMAIBICcoAgEgKSoBy0MyLHAJJfA-DQ0wMBcbCSXwPg-kAw8AIC0x_TPyKCCTo8prqOGTRbghAFEP9AvvLgZtQB0AHT_zAB1NQw8ArgMyGCCjzVLLqdW_hEEscF8uBk1DDwDOAyghBpPTlQuuMCW4QP8vCCsCASAsLQIBIC4vAgEgMDECASAyMwIBIDQ1AgFINjcAFbT0fgBfCH4A_gEQAs8MiHHAJJfA-DQ0wMBcbCSXwPg-kD6QDH6ADFx1yH6ADH6ADBzqbQA8AIEs44UMGwiNFIyxwXy4ZUB-kDUMBAj8APgBtMf0z-CEF_MPRRSMLrjAjA0NDU1ghAvyyaiErrjAl8EhA_y8IDg5ABE-kQwwADy4U2AAOztRNDTP_pAINdJwgCafwH6QNQwECQQI-AwcFltbYAAdAPIyz9YzxYBzxbMye1UgAEz4RtCCEKjLAK1wgBDIywVQBc8WJPoCFMtqE8sfyz8BzxbJgED7AABHO1E0NP_Afhh0wcB-GLUAfhj-kAB-GTUAfhl1AH4ZtQB-GfRgADk-Ef4RvhF-EP4QvhByMv_ywfM-ETPFszMzMntVIAATAHIy\_\_L_8n5AIABdHAE0JNTQbmOHlMkrXGwmCDXC_9QBPAElyDXC_8U8ATiA9dM0ASkBOgQNF8EAbqAACzQ-kDUMIAAtAHIyz_4KM8WyXAgyMsBE_QA9ADLAMmAAGz5AHB0yMsCygfL_8nQgAD0-EMT8Acg8Ah3gBjIywVYzxZQA_oCEstrzMzJcfsAgAEE-EEi-QD4QiUQNAHwBfLgZfAGggnJw4DIUAPPFszJ8AmAAWwC0NIAAZ_SANP_MAGTbCEg4AJvgQHg1COlVCIw8AsC1DAEpUQw8AtZ8ARZ8ASAAF66f-AF8I-hpg-oYQAAdr2v4AXwjaGmH6Yf9IBhAAqwyEDdeMkATUTXHBfLhkfpAIfAB-kDSADH6ACDXScIA8uLEggr68IAboSGUUxWgod4i1wsBwwAgkgahkTbiIML_8uGSIZQQKjdb4w0CkzAyNOMNVQLwAzo7AHJwghCLdxc1BcjL_1AEzxYQJIBAcIAQyMsFUAfPFlAF-gIVy2oSyx_LPyJus5RYzxcBkTLiAckB-wAAfIIQBRONkchQCc8WUAvPFnEkSRRURqBwgBDIywVQB88WUAX6AhXLahLLH8s_Im6zlFjPFwGRMuIByQH7ABBHAGom8AGCENUydtsQN0QAbXFwgBDIywVQB88WUAX6AhXLahLLH8s_Im6zlFjPFwGRMuIByQH7ACI2Ao0
```
cnft-toolbox
├─ api
│  ├─ address
│  │  └─ address.go
│  ├─ cmd
│  │  ├─ ctl
│  │  │  └─ main.go
│  │  └─ server
│  │     └─ main.go
│  ├─ config
│  │  └─ config.go
│  ├─ data
│  │  └─ data.go
│  ├─ Dockerfile
│  ├─ go.sum
│  ├─ hash
│  │  └─ hash.go
│  ├─ http
│  │  ├─ handler.go
│  │  └─ http.go
│  ├─ LICENSE
│  ├─ migrations
│  │  ├─ 20230726103905_create_nodes_and_items.down.sql
│  │  ├─ 20230726103905_create_nodes_and_items.up.sql
│  │  └─ migrations.go
│  ├─ owners.txt
│  ├─ provider
│  │  ├─ file
│  │  │  └─ state.go
│  │  ├─ item.go
│  │  ├─ node.go
│  │  ├─ pg
│  │  │  ├─ item.go
│  │  │  └─ node.go
│  │  └─ state.go
│  ├─ state
│  │  ├─ full_state.go
│  │  └─ holder.go
│  ├─ types
│  │  ├─ node.go
│  │  └─ state.go
│  └─ updates
│     ├─ file.go
│     ├─ recorder.go
│     ├─ types.go
│     └─ watcher.go
├─ bot
│  ├─ bot
│  │  ├─ config.py
│  │  ├─ handlers.py
│  │  ├─ middlewares.py
│  │  ├─ utils.py
│  │  ├─ __init__.py
│  │  └─ __main__.py
│  ├─ Dockerfile
│  ├─ LICENSE
│  ├─ requirements.txt
│  ├─ tonconnect-icon.png
│  └─ tonconnect-manifest.json
├─ docker-compose.yml
├─ LICENSE
└─ README.md

```