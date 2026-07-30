import os

def cleanup():
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_dir = os.path.join(workspace_root, "database")

    old_files = [
        "usmle_step1.db",
        "usmle_step2_ck.db",
        "fcps_nle_medical.db",
        "plab_ukmla.db",
        "neet_pg_fmge.db",
        "surgery_mrcs.db",
        "pharmacology_pg.db",
        "basic_sciences_anatomy_physio.db",
        "fcps_qbank.db"
    ]

    for f_name in old_files:
        p = os.path.join(db_dir, f_name)
        if os.path.exists(p):
            try:
                os.remove(p)
                print(f"Removed old snake_case file: {f_name}")
            except Exception as e:
                print(f"Could not remove {f_name}: {e}")

if __name__ == "__main__":
    cleanup()
