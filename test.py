from core.snowflake import SnowflakeGenerator


generator = SnowflakeGenerator(1)
for _ in range(1000):
    generated_id = generator.generate()
    print(f'Generated Id: {generated_id}')
