"""
Master AI - Phase 7.2 Professional Open-Source Asset Ingestion & Management Engine
Supports: Poly Haven, ambientCG, Smithsonian 3D, NASA 3D, Wikimedia Commons.
Enforces strict license auditing, SHA-256 integrity, provenance recording,
and automated quarantine of non-commercial or ambiguous assets.
"""

import os
import sys
import json
import hashlib
import time
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger("MasterAI.AssetPipeline")
logging.basicConfig(level=logging.INFO)

CATALOG_PATH = r"F:\Master AI\15_ASSETS\open_source_library\asset_catalog.json"
LIBRARY_BASE_DIR = r"F:\Master AI\15_ASSETS\open_source_library"

# Permissible licenses for commercial autonomous video production
PERMITTED_COMMERCIAL_LICENSES = {
    "CC0", "CC0 1.0", "Public Domain", "NASA Public Domain", 
    "Smithsonian CC0", "CC BY 4.0", "CC BY 3.0", "CC BY 2.0", "Pexels License"
}

# Licenses requiring quarantine and human legal review before commercial publication
QUARANTINE_LICENSES = {
    "CC BY-NC", "CC BY-NC 4.0", "CC BY-NC-SA", "CC BY-NC-ND",
    "CC BY-ND", "CC BY-SA 4.0", "CC BY-SA 3.0", "Editorial Use Only"
}

class AssetIngestionManager:
    """Enterprise open-source 3D and multimedia asset ingestion manager."""
    
    def __init__(self, catalog_path: str = CATALOG_PATH):
        self.catalog_path = catalog_path
        self.catalog = self._load_catalog()

    def _load_catalog(self) -> Dict[str, Any]:
        if os.path.isfile(self.catalog_path):
            try:
                with open(self.catalog_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load catalog: {e}")
        return {"version": "1.0.0-phase7.2", "updated_at": datetime.now().isoformat(), "assets": {}}

    def _save_catalog(self):
        os.makedirs(os.path.dirname(self.catalog_path), exist_ok=True)
        self.catalog["updated_at"] = datetime.now().isoformat()
        with open(self.catalog_path, "w", encoding="utf-8") as f:
            json.dump(self.catalog, f, indent=2)

    @staticmethod
    def compute_sha256(filepath: str) -> str:
        """Compute SHA-256 hash of a file."""
        hasher = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()

    def audit_license(self, license_name: str) -> Dict[str, Any]:
        """Audit a license string and determine clearance status."""
        lic = license_name.strip()
        
        # Check explicit quarantine
        for q in QUARANTINE_LICENSES:
            if q.lower() in lic.lower():
                return {
                    "status": "QUARANTINED",
                    "commercial_allowed": False,
                    "modification_allowed": False if "ND" in lic.upper() else True,
                    "attribution_required": True,
                    "reason": f"License '{lic}' contains Non-Commercial, ShareAlike, or No-Derivatives restrictions."
                }
                
        # Check permitted licenses
        for p in PERMITTED_COMMERCIAL_LICENSES:
            if p.lower() in lic.lower():
                is_cc0_pd = "CC0" in p or "Public Domain" in p
                return {
                    "status": "APPROVED",
                    "commercial_allowed": True,
                    "modification_allowed": True,
                    "attribution_required": not is_cc0_pd,
                    "reason": "Permissive commercial license verified."
                }
                
        # Unknown license
        return {
            "status": "QUARANTINED",
            "commercial_allowed": False,
            "modification_allowed": False,
            "attribution_required": True,
            "reason": f"Unrecognized license '{lic}'. Quarantined by default."
        }

    def register_asset(
        self,
        asset_id: str,
        title: str,
        category: str,
        source_repo: str,
        source_url: str,
        creator: str,
        license_name: str,
        local_file_path: str,
        tags: Optional[List[str]] = None,
        technical_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Register a verified asset into the Master AI open-source library.
        Validates file existence, computes SHA-256, audits license, and updates catalog.
        """
        if not os.path.isfile(local_file_path):
            raise FileNotFoundError(f"Local asset file does not exist: {local_file_path}")

        audit = self.audit_license(license_name)
        sha256_hash = self.compute_sha256(local_file_path)
        file_size = os.path.getsize(local_file_path)

        record = {
            "asset_id": asset_id,
            "title": title,
            "category": category, # e.g. '3d_animal', 'pbr_material', 'hdri', 'scientific_3d'
            "source_repo": source_repo,
            "source_url": source_url,
            "creator": creator,
            "license": license_name,
            "commercial_allowed": audit["commercial_allowed"],
            "modification_allowed": audit["modification_allowed"],
            "attribution_required": audit["attribution_required"],
            "attribution_text": f"'{title}' by {creator} ({source_repo}), licensed under {license_name}. Source: {source_url}" if audit["attribution_required"] else f"'{title}' ({source_repo}, {license_name})",
            "quarantine_status": audit["status"],
            "quarantine_reason": audit["reason"],
            "sha256": sha256_hash,
            "file_size_bytes": file_size,
            "local_path": os.path.abspath(local_file_path),
            "download_date": datetime.now().isoformat(),
            "tags": tags or [],
            "technical_metadata": technical_metadata or {}
        }

        self.catalog["assets"][asset_id] = record
        self._save_catalog()
        logger.info(f"Registered asset [{asset_id}] - Status: {audit['status']} ({license_name})")
        return record

    def get_asset(self, asset_id: str) -> Optional[Dict[str, Any]]:
        return self.catalog["assets"].get(asset_id)

    def search_assets(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        only_approved: bool = True
    ) -> List[Dict[str, Any]]:
        """Search catalog with optional category and commercial approval filtering."""
        results = []
        q_lower = query.lower() if query else ""
        
        for aid, rec in self.catalog["assets"].items():
            if only_approved and rec.get("quarantine_status") != "APPROVED":
                continue
            if category and rec.get("category") != category:
                continue
            if query:
                match = (
                    q_lower in rec.get("title", "").lower() or
                    q_lower in aid.lower() or
                    any(q_lower in t.lower() for t in rec.get("tags", []))
                )
                if not match:
                    continue
            results.append(rec)
        return results

    def generate_credits_manifest(self, used_asset_ids: List[str]) -> Dict[str, Any]:
        """Generate legal credits and attribution manifest for a video production."""
        attributions = []
        quarantined_warnings = []
        
        for aid in used_asset_ids:
            asset = self.get_asset(aid)
            if not asset:
                continue
            if asset.get("quarantine_status") == "QUARANTINED":
                quarantined_warnings.append(f"WARNING: Asset '{aid}' is quarantined ({asset.get('quarantine_reason')})")
            if asset.get("attribution_required"):
                attributions.append(asset["attribution_text"])
                
        return {
            "total_assets_used": len(used_asset_ids),
            "attributions_count": len(attributions),
            "attributions": attributions,
            "quarantined_warnings": quarantined_warnings,
            "is_commercially_cleared": len(quarantined_warnings) == 0
        }

if __name__ == "__main__":
    mgr = AssetIngestionManager()
    print("Asset Ingestion Manager initialized. Total registered assets:", len(mgr.catalog["assets"]))
