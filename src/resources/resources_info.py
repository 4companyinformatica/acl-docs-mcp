from src.resources.resources_names import resources_names
from textwrap import dedent


general_directives = dedent("""
    ## Diretivas Gerais:
    The resources from this server, are made to improve the quality of generated ACL Scripts, to use it right, first, search for the file using {list_resource}, then retrieve its contents with {get_resource}
""").strip().format(
    list_resource=resources_names['mcpr_list_acl_script_examples'],
    get_resource=resources_names['mcpr_get_acl_script_example'],
)

resources_info = {
    "mcpr_list_acl_script_examples": {
        "uri": "arquivos://assets/acl_examples",
        "name": resources_names['mcpr_list_acl_script_examples'],
        "description": dedent("""
            {directives}

            ## Description
            Fetches the list of ACL scripts to be used as examples/models
        """).strip().format(directives=general_directives),
        "mime_type": "application/json"
    },
# ==================================================
    "mcpr_get_acl_script_example": {
        "uri": "arquivos://assets/acl_examples/{nome_arquivo}",
        "name": resources_names['mcpr_get_acl_script_example'],
        "description": dedent("""
            {directives}

            ## Description
            Return the acl script resource content
        """).strip().format(directives=general_directives),
        "mime_type": "text/plain"
    }
}
