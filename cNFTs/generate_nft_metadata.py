import json
import os


def generate_nft_metadata(output_folder="nft_metadata", total_files=10):
    os.makedirs(output_folder, exist_ok=True)

    base_metadata = {
        "description": "Special hand-drawn, 3d rendered and animated Access Passes, created specially to reward our OG Telegram Community with 1 year of free access to our Telegram Mini App on The Open Network and much more!",
        "image": "https://divercitylabs.duckdns.org/collections/cc4f1d7be4187d53532d57aa/nft/image.webp",
        "animation_url": "https://divercitylabs.duckdns.org/collections/cc4f1d7be4187d53532d57aa/nft/animation.mp4",
        "attributes": [
            {"trait_type": "Material", "value": "3D Plastic"},
            {"trait_type": "Teleclubber", "value": "OG"},
        ],
    }

    for i in range(total_files):
        metadata = {"name": f"TCLUB PASS #{i}", **base_metadata}
        file_path = os.path.join(output_folder, f"{i}.json")

        with open(file_path, "w") as json_file:
            json.dump(metadata, json_file, indent=2)

    print(
        f"{total_files} JSON metadata files have been generated in '{output_folder}' folder."
    )


# Run the script
generate_nft_metadata()
