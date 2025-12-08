
lms_module = {
	"collection": "lms_module",
	"meta": {
		"collection": "lms_module",
        "group": "lms_content",
		"icon": "tab_group",
		"note": "The collection for the modules",
		"hidden": False,
		"singleton": False,
		"translations": [
			{
				"language": "en-US",
				"translation": "module"
			}
		],
	},
	"schema": {
		"name": "lms_module",
		"comment": None
	},
	"fields": [
    {
      "field": "id",
      "type": "uuid",
      "meta": {
        "icon": "id",
        "readonly": True,  # Make it read-only to prevent editing
        "hidden": True      # Hide it in the Data Studio UI
      },
      "schema": {
        "is_primary_key": True,
        "is_nullable": False
      }
    }
	]
}

lms_modules_fields = [
    {
        "collection": "lms_module",
        "field": "status",
        "type": "string",
        "meta": {
            "collection": "lms_module",
            "field": "status",
            "interface": "select-dropdown",
            "options": {"choices": ["draft", "published", "archived"]},
            "required": True,
            "default_value": "draft",
            "sort": 1,
            "width": "half-space",
            "note": "Status of the module"
        },
        "schema": {
            "name": "status",
            "table": "lms_module",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": False
        }
    },
    {
        "collection": "lms_module",
        "field": "sort",
        "type": "integer",
        "meta": {
            "collection": "lms_module",
            "field": "sort",
            "interface": "input",
            "sort": 2,
            "width": "half",
            "hidden": True,
            "note": "Sorting order of the module"
        },
        "schema": {
            "name": "sort",
            "table": "lms_module",
            "data_type": "integer",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_module",
        "field": "date_created",
        "type": "timestamp",
        "meta": {
            "collection": "lms_module",
            "field": "date_created",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 3,
            "width": "half",
            "note": "The date when the module was created"
        },
        "schema": {
            "name": "date_created",
            "table": "lms_module",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_module",
        "field": "date_updated",
        "type": "timestamp",
        "meta": {
            "collection": "lms_module",
            "field": "date_updated",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 4,
            "width": "half",
            "note": "The date when the module was last updated"
        },
        "schema": {
            "name": "date_updated",
            "table": "lms_module",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_module",
        "field": "title",
        "type": "string",
        "meta": {
            "collection": "lms_module",
            "field": "title",
            "interface": "input",
            "sort": 5,
            "width": "full",
            "note": "Title of the module",
            "required": True
        },
        "schema": {
            "name": "title",
            "table": "lms_module",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_module",
        "field": "description",
        "type": "text",
        "meta": {
            "collection": "lms_module",
            "field": "description",
            "interface": "wysiwyg",
            "sort": 6,
            "width": "full",
            "note": "Description of the module"
        },
        "schema": {
            "name": "description",
            "table": "lms_module",
            "data_type": "text",
            "is_nullable": True
        }
    }
]

lms_module_relation_data = {

    "collection": "lms_module",  # The "many" side collection
    "field": "course",  # Field in lms_module that references the course
    "related_collection": "lms_course",  # The "one" side collection
    "meta": {
        "many_collection": "lms_module",
        "many_field": "course",
        "one_collection": "lms_course",
        "one_field": "modules",  # Optional: field on the course side referencing modules
        "one_deselect_action": "nullify"  # What happens when a course is deleted
    }
}