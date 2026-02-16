import pyarrow.parquet as pq

# Read schemas from all three taxi types
yellow_schema = pq.read_schema('data/yellow/yellow_tripdata_2019-01.parquet')
green_schema = pq.read_schema('data/green/green_tripdata_2019-01.parquet')
fhv_schema = pq.read_schema('data/fhv/fhv_tripdata_2019-01.parquet')

# Convert schemas to lists of (name, type) tuples
yellow_fields = [(field.name, str(field.type)) for field in yellow_schema]
green_fields = [(field.name, str(field.type)) for field in green_schema]
fhv_fields = [(field.name, str(field.type)) for field in fhv_schema]

# Get all unique field names
yellow_field_names = set([f[0] for f in yellow_fields])
green_field_names = set([f[0] for f in green_fields])
fhv_field_names = set([f[0] for f in fhv_fields])
all_field_names = sorted(yellow_field_names | green_field_names | fhv_field_names)

# Create dictionaries for easy lookup
yellow_dict = dict(yellow_fields)
green_dict = dict(green_fields)
fhv_dict = dict(fhv_fields)

# Prepare output
output = []
output.append("=" * 120)
output.append("TAXI DATA SCHEMA COMPARISON - YELLOW vs GREEN vs FHV")
output.append("=" * 120)
output.append("")
output.append(f"{'Field Name':<35} {'Yellow Taxi':<25} {'Green Taxi':<25} {'FHV Taxi':<25}")
output.append("-" * 120)

# Compare field by field
only_yellow = []
only_green = []
only_fhv = []
type_differences = []
common_fields = []

for field_name in all_field_names:
    yellow_type = yellow_dict.get(field_name, "NOT PRESENT")
    green_type = green_dict.get(field_name, "NOT PRESENT")
    fhv_type = fhv_dict.get(field_name, "NOT PRESENT")
    
    # Check which datasets have this field
    present_in = []
    if yellow_type != "NOT PRESENT":
        present_in.append("yellow")
    if green_type != "NOT PRESENT":
        present_in.append("green")
    if fhv_type != "NOT PRESENT":
        present_in.append("fhv")
    
    # Mark exclusivity
    note = ""
    if len(present_in) == 1:
        if present_in[0] == "yellow":
            only_yellow.append(field_name)
            note = " << YELLOW ONLY"
        elif present_in[0] == "green":
            only_green.append(field_name)
            note = " << GREEN ONLY"
        elif present_in[0] == "fhv":
            only_fhv.append(field_name)
            note = " << FHV ONLY"
    elif len(present_in) == 3:
        # Check if types differ
        if yellow_type == green_type == fhv_type:
            common_fields.append(field_name)
        else:
            type_differences.append((field_name, yellow_type, green_type, fhv_type))
            note = " << TYPE DIFF"
    else:
        # Present in 2 out of 3
        if yellow_type != green_type or yellow_type != fhv_type or green_type != fhv_type:
            type_differences.append((field_name, yellow_type, green_type, fhv_type))
            note = " << TYPE DIFF"
    
    output.append(f"{field_name:<35} {yellow_type:<25} {green_type:<25} {fhv_type:<25}{note}")

# Summary section
output.append("")
output.append("=" * 120)
output.append("SUMMARY OF DIFFERENCES")
output.append("=" * 120)
output.append("")

output.append(f"Total fields in Yellow Taxi: {len(yellow_fields)}")
output.append(f"Total fields in Green Taxi: {len(green_fields)}")
output.append(f"Total fields in FHV Taxi: {len(fhv_fields)}")
output.append(f"Common fields (all three): {len(common_fields)}")
output.append("")

if only_yellow:
    output.append(f"Fields ONLY in Yellow Taxi ({len(only_yellow)}):")
    for field in only_yellow:
        output.append(f"  - {field} ({yellow_dict[field]})")
    output.append("")

if only_green:
    output.append(f"Fields ONLY in Green Taxi ({len(only_green)}):")
    for field in only_green:
        output.append(f"  - {field} ({green_dict[field]})")
    output.append("")

if only_fhv:
    output.append(f"Fields ONLY in FHV Taxi ({len(only_fhv)}):")
    for field in only_fhv:
        output.append(f"  - {field} ({fhv_dict[field]})")
    output.append("")

if type_differences:
    output.append(f"Fields with DIFFERENT TYPES ({len(type_differences)}):")
    for field, y_type, g_type, f_type in type_differences:
        output.append(f"  - {field}:")
        output.append(f"      Yellow: {y_type}")
        output.append(f"      Green:  {g_type}")
        output.append(f"      FHV:    {f_type}")
    output.append("")

if not only_yellow and not only_green and not only_fhv and not type_differences:
    output.append("No differences found! Schemas are identical.")

# Write to file
with open('schema_comparison.txt', 'w') as f:
    f.write('\n'.join(output))

print("Schema comparison saved to: schema_comparison.txt")
print(f"\nQuick Summary:")
print(f"  Yellow fields: {len(yellow_fields)}")
print(f"  Green fields: {len(green_fields)}")
print(f"  FHV fields: {len(fhv_fields)}")
print(f"  Fields only in yellow: {len(only_yellow)}")
print(f"  Fields only in green: {len(only_green)}")
print(f"  Fields only in FHV: {len(only_fhv)}")
print(f"  Type differences: {len(type_differences)}")
