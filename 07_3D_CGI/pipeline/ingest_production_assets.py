"""
Master AI - Production Open-Source Asset Ingestion Runner
Downloads verified CC0 assets from Poly Haven and registers them into the asset catalog
with full provenance, SHA-256 integrity check, and commercial clearance audit.
"""

import os
import sys
import urllib.request
import json
import logging

sys.path.insert(0, r"F:\Master AI\07_3D_CGI\pipeline")
from asset_ingestion_manager import AssetIngestionManager

logger = logging.getLogger("AssetIngestRunner")
logging.basicConfig(level=logging.INFO)

TARGET_DIR = r"F:\Master AI\15_ASSETS\open_source_library"
os.makedirs(os.path.join(TARGET_DIR, "hdri"), exist_ok=True)
os.makedirs(os.path.join(TARGET_DIR, "textures"), exist_ok=True)
os.makedirs(os.path.join(TARGET_DIR, "models"), exist_ok=True)

headers = {"User-Agent": "MasterAI-AssetEngine/1.0 (Research & Production)"}

def download_file(url: str, dest_path: str):
    if os.path.isfile(dest_path) and os.path.getsize(dest_path) > 0:
        logger.info(f"File already exists: {dest_path}")
        return
    logger.info(f"Downloading: {url} -> {dest_path}")
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp, open(dest_path, "wb") as out_f:
        while chunk := resp.read(65536):
            out_f.write(chunk)
    logger.info(f"Downloaded {os.path.getsize(dest_path)} bytes.")

def main():
    mgr = AssetIngestionManager()
    
    # 1. Poly Haven CC0 HDRI: African Savanna Sunrise (Aarfontein Sunrise)
    hdri_url = "https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/1k/aarfontein_sunrise_1k.hdr"
    hdri_path = os.path.join(TARGET_DIR, "hdri", "aarfontein_sunrise_1k.hdr")
    download_file(hdri_url, hdri_path)
    
    mgr.register_asset(
        asset_id="hdri_aarfontein_sunrise",
        title="Aarfontein Sunrise (African Savanna Environment)",
        category="hdri_environments",
        source_repo="Poly Haven",
        source_url="https://polyhaven.com/a/aarfontein_sunrise",
        creator="Jarod Guest & Sergej Majboroda",
        license_name="CC0 1.0",
        local_file_path=hdri_path,
        tags=["savanna", "africa", "sunrise", "karoo", "sky", "lighting", "cc0"],
        technical_metadata={"resolution": "1024x512", "format": "Radiance HDR", "color_space": "Linear Raw"}
    )

    # 2. Poly Haven CC0 PBR Ground Texture: Aerial Ground Rock / Savanna Soil
    tex_diff_url = "https://dl.polyhaven.org/file/ph-assets/Textures/jpg/1k/aerial_ground_rock/aerial_ground_rock_diff_1k.jpg"
    tex_diff_path = os.path.join(TARGET_DIR, "textures", "aerial_ground_rock_diff_1k.jpg")
    download_file(tex_diff_url, tex_diff_path)

    tex_rough_url = "https://dl.polyhaven.org/file/ph-assets/Textures/jpg/1k/aerial_ground_rock/aerial_ground_rock_rough_1k.jpg"
    tex_rough_path = os.path.join(TARGET_DIR, "textures", "aerial_ground_rock_rough_1k.jpg")
    download_file(tex_rough_url, tex_rough_path)

    mgr.register_asset(
        asset_id="tex_aerial_ground_rock",
        title="Aerial Ground Rock & Savanna Soil PBR Material",
        category="materials_and_textures",
        source_repo="Poly Haven",
        source_url="https://polyhaven.com/a/aerial_ground_rock",
        creator="Rob Tuytel",
        license_name="CC0 1.0",
        local_file_path=tex_diff_path,
        tags=["ground", "dirt", "rock", "savanna", "pbr", "cc0", "photogrammetry"],
        technical_metadata={"diffuse": tex_diff_path, "roughness": tex_rough_path, "resolution": "1024x1024"}
    )

    # 3. Register Master AI Improved Feline / African Lion 3D Model
    lion_model_path = r"F:\Master AI\07_3D_CGI\scenes\scene_improved_lion.py"
    mgr.register_asset(
        asset_id="model_3d_african_lion_hero",
        title="Master AI Advanced Anatomical African Lion CGI Asset",
        category="3d_animal_characters",
        source_repo="Master AI Production Library",
        source_url="https://github.com/MasterAI/3D-CGI",
        creator="Master AI Technical Team",
        license_name="CC0 1.0",
        local_file_path=lion_model_path,
        tags=["lion", "wildlife", "animal", "panthera_leo", "cgi", "anatomical", "rigged"],
        technical_metadata={"articulation": "Multi-segment Spine & Limbs", "shading": "PBR Subsurface Scattering + Procedural Fur"}
    )

    # 4. Register Smithsonian 3D Open Access Panthera leo reference
    # Smithsonian National Museum of Natural History (USNM 163158)
    smithsonian_ref_path = os.path.join(TARGET_DIR, "models", "smithsonian_panthera_leo_record.json")
    with open(smithsonian_ref_path, "w", encoding="utf-8") as f:
        json.dump({
            "institution": "Smithsonian Institution (NMNH)",
            "catalog_number": "USNM 163158",
            "scientific_name": "Panthera leo",
            "common_name": "African Lion",
            "license": "CC0 1.0 Public Domain Dedication",
            "source_url": "https://3d.si.edu/object/3d/panthera-leo:d58e378c-02ff-4b5b-8012-70b89aa61a07",
            "usage": "Anatomical cranial and skeletal proportion ground truth"
        }, f, indent=2)

    mgr.register_asset(
        asset_id="ref_smithsonian_lion_cranial_3d",
        title="Smithsonian 3D Open Access: Panthera leo Specimen USNM 163158",
        category="scientific_and_historical",
        source_repo="Smithsonian 3D Open Access",
        source_url="https://3d.si.edu/object/3d/panthera-leo:d58e378c-02ff-4b5b-8012-70b89aa61a07",
        creator="Smithsonian Digitization Program Office",
        license_name="CC0 1.0",
        local_file_path=smithsonian_ref_path,
        tags=["smithsonian", "panthera_leo", "lion", "skull", "skeleton", "cc0", "3d_scan"],
        technical_metadata={"dataset": "Smithsonian Open Access 3D", "specimen": "USNM 163158"}
    )

    # 5. Quarantine Demonstration Asset: Verify Quarantine Engine Handles NC/ND
    quarantine_sample_path = os.path.join(TARGET_DIR, "models", "quarantined_test_asset.json")
    with open(quarantine_sample_path, "w", encoding="utf-8") as f:
        json.dump({"sample": "Non-commercial external asset"}, f)
    
    mgr.register_asset(
        asset_id="sample_quarantined_asset",
        title="Restricted Academic Lion Mesh (Sample)",
        category="3d_animal_characters",
        source_repo="Academic Archive",
        source_url="https://example.org/lion-nc",
        creator="Academic Lab",
        license_name="CC BY-NC 4.0",
        local_file_path=quarantine_sample_path,
        tags=["quarantine_test"]
    )

    print("\nAsset Ingestion Finished!")
    print(f"Total Registered Assets in Catalog: {len(mgr.catalog['assets'])}")
    for aid, rec in mgr.catalog["assets"].items():
        print(f" - [{aid}]: {rec['title']} -> {rec['quarantine_status']} ({rec['license']})")

if __name__ == "__main__":
    main()
