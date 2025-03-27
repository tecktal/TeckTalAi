
lms_topic = {
	"collection": "lms_topic",
	"meta": {
		"collection": "lms_topic",
        "group": "lms_metadata",
		"icon": "tag",
		"note": "The collection for the topics",
		"hidden": False,
		"singleton": False,
		"translations": [
			{
				"language": "en-US",
				"translation": "topic"
			}
		],
	},
	"schema": {
		"name": "lms_topic",
		"comment": None
	},
	"fields": [
    {
      "field": "id",
      "type": "uuid",
      "meta": {
        "icon": "id",
        "readonly": True,
        "hidden": True
      },
      "schema": {
        "is_primary_key": True,
        "is_nullable": False
      }
    }
	]
}

lms_topics_fields = [
    {
        "collection": "lms_topic",
        "field": "date_created",
        "type": "timestamp",
        "meta": {
            "collection": "lms_topic",
            "field": "date_created",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 1,
            "width": "half",
            "note": "The date when the topic was created"
        },
        "schema": {
            "name": "date_created",
            "table": "lms_topic",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_topic",
        "field": "date_updated",
        "type": "timestamp",
        "meta": {
            "collection": "lms_topic",
            "field": "date_updated",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 2,
            "width": "half",
            "note": "The date when the topic was last updated"
        },
        "schema": {
            "name": "date_updated",
            "table": "lms_topic",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_topic",
        "field": "title",
        "type": "string",
        "meta": {
            "collection": "lms_topic",
            "field": "title",
            "interface": "input",
            "sort": 3,
            "width": "full",
            "note": "Title of the topic",
            "required": True
        },
        "schema": {
            "name": "title",
            "table": "lms_topic",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_topic",
        "field": "slug",
        "type": "string",
        "meta": {
            "collection": "lms_topic",
            "field": "slug",
            "interface": "input",
            "sort": 4,
            "width": "full",
            "note": "URL-friendly identifier for the topic",
            "required": True
        },
        "schema": {
            "name": "slug",
            "table": "lms_topic",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_topic",
        "field": "description",
        "type": "text",
        "meta": {
            "collection": "lms_topic",
            "field": "description",
            "interface": "textarea",
            "sort": 5,
            "width": "full",
            "note": "Description of the topic"
        },
        "schema": {
            "name": "description",
            "table": "lms_topic",
            "data_type": "text",
            "is_nullable": True
        }
    }
]