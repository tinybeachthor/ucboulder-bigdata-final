setup: dbs

dbs: db_content_migrate

db_content_migrate:
	FLYWAY_CLEAN_DISABLED=false \
	flyway \
	-user=guest -password=guest \
	-url="jdbc:postgresql://localhost:5432/content" \
	-locations=filesystem:databases/content \
	clean migrate
