setup: dbs_clean dbs_migrate

dbs_migrate: db_content_migrate

dbs_clean: db_content_clean

db_content_migrate:
	flyway \
	-user=guest -password=guest \
	-url="jdbc:postgresql://localhost:5432/content" \
	-locations=filesystem:databases/content \
	migrate

db_content_clean:
	FLYWAY_CLEAN_DISABLED=false \
	flyway \
	-user=guest -password=guest \
	-url="jdbc:postgresql://localhost:5432/content" \
	-locations=filesystem:databases/content \
	clean
