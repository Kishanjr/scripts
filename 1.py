INSERT INTO synapt_dev_db.usecase_metrics (
    entity_type, ticket, channel, description, vast_id, entity_value, updated_time
)
VALUES (%s, %s, %s, %s, %s, %s, '2024-12-23 07:25:00')
ON CONFLICT (entity_type, ticket, channel, description, vast_id)
DO UPDATE SET
    entity_value = EXCLUDED.entity_value,
    updated_time = EXCLUDED.updated_time;
