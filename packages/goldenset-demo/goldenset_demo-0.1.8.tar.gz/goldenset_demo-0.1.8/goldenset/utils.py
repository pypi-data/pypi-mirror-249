from typing import List, Dict
from .goldenset import get_supabase_client


def get_run_data(run_id: str) -> List[Dict]:
    supabase = get_supabase_client()
    resp = supabase.table("run_row").select("*").eq("run_id", run_id).execute()
    return resp.data


def delete_run(run_id: str) -> bool:
    """Returns True if the run was deleted, False if it was not found"""
    supabase = get_supabase_client()
    resp = supabase.table("run_row").delete().eq("run_id", run_id).execute()
    return len(resp.data) > 0
