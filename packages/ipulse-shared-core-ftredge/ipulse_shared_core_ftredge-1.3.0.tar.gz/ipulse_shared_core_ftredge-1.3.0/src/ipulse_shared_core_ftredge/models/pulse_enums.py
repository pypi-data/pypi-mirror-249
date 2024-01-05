organisation_relations = { 
    "*",
    "retail_customer",
    "corporate_customer",
    "parent",
    "sister",
    "self",
    "partner",
    "supplier",
    "sponsor",
    "investor",
    "regulator",
    "other"
    }

organisation_industries  = {
    "*",
    "data",
    "government",
    "media",
    "academic",
    "commercial",
    "fund",
    "finance",
    "advisory",
    "hedgefund",
    "bank",
    "vc",
    "pe",
    "construction",
    "healthcare",
    "technology",
    "consulting",
    "retail",
    "non_profit",
    "individual",
    "freelancer",
    "other"
}


resource_classifications = {
    "*",
    "public",
    "auth_required_open", # synthetic data , prices of gold etc.
    "auth_required_restricted", ##special features 
    "auth_required_confidential", ## user data etc. 
    "internal_only_open", ## internal public reports, emails etc. 
    "internal_only_restricted", ##internal financials summary reports , web and app analytics, lsit of admin users etc.
    "internal_only_confidential", ## source data : key financials, salaries and bonuses etc
    "top_confidential"  ##secrets, admin passwords etc.
}

effects={"allow", "deny"}

actions ={
          "create",
          "batch_create",
          "read", 
          "batch_read",
          "update",
          "batch_update",
          "add",
          "batch_add",
          "remove",
          "batch_remove",
          "delete",
          "batch_delete", 
          "rename" ,
          "batch_rename",
          "move",
          "batch_move",
          "download",
          "upload",
          "share"
                }


resource_types =  {
    "db", "sql_db", "nosql_db", "dynamodb",
    "big_query", "big_query_project", "big_query_table", "big_query_column", 
    "big_query_row", "big_query_cell",
    "firestore", "firestore_project", "firestore_collection", 
    "firestore_document","firestore_document_with_timeseries" "firestore_document_field",
    "pandas_dataframe", "spark_dataframe",
    "s3_bucket", "storage_bucket",
    "folder", "file", "json_file", "csv_file", "pdf_file", 
    "unstructured_file", "image", "video", "audio", "text",
    "api", "report", "dashboard", "webpage", "website", "web"
}


resource_origins = {"*", "internal", "external", "mixed"}

resource_original_or_processed = {"*", 
                                 "original_source", 
                                 "original_copy", 
                                 "processed_source", # Example User Profiles
                                 "processed_copy", 
                                 "mixed_source",
                                 "mixed_copy" }

resource_contents = {
    "*",
    "synthetic_data",
    "composite_data",
    "user_core_profile"
    "user_generated_shareable",
    "user_owned_shareable",
    "user_generated_private",
    "user_owned_private",
    "organisation_profile",
    "mlprediction",
    "mlmetrics",
    "internal_report",
    "system_generated",
    "our_financials"
}

resource_readable_by={
    "*",
    "all",
    "authenticated",
    "restircted",
    "owner",
    "selected_by_owner",
    "admin",
    "selected_by_admin",
    "super_admin",
    "super_admin_selected",
    "system"
}

resource_updatable_by={
     "*",
    "all",
    "authenticated",
    "restircted",
    "owner",
    "selected_by_owner",
    "admin",
    "selected_by_admin",
    "super_admin",
    "super_admin_selected",
    "system"
}

pulse_modules={
    "*",
    "core",
    "gym",
    "orcl",
    "scen",
    "invs",
    "prfl",
    "trde",
    "bet",
    "chat"
}

licences_types={
    "*",
    ######################################### OPEN or FULL Rights
    "public",
    "open",
    "open_no_tandc",
    "full_rights",
    "full_rights_for_sale",
    "commercial_licence_perpetual",
    "customer_private_tac",
    ######################################### SPECIAL CONDITIONS
    "open_with_tandc",
    "on_special_request",
    "commercial_licence_limited_time",
    "customer_owned_for_sale",
     ######################################### Not for Commercial Use
    "full_rights_not_for_sale",
    "internal_only",
    "academic_licence",
    "not_for_commercial_use",
    "customer_private"
    ######################################### Unknown
    "commercial_licence_not_purchased",
    "web_scrapped",
    "unknown"
}

