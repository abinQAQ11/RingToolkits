import sdds
from pathlib import Path

def get_unique_filename(file_name, extension=".txt"):
    counter = 0
    path = Path(f"{file_name}_params_{counter}{extension}")

    # 如果文件已存在，递增数字后缀
    while path.exists():
        path = Path(f"{file_name}_params_{counter}{extension}")
        counter += 1

    return str(path)

def read(sdds_name):
    # Specify the input SDDS file.
    input_file = sdds_name

    # Load the SDDS file into the SDDS object
    sdds_obj = sdds.load(input_file)

    # Open a file for writing
    file_name = Path(input_file).stem
    output_file = get_unique_filename(file_name)

    with open(output_file, "w") as f:
        # Determine and display the file mode: Binary or ASCII
        if sdds_obj.mode == sdds.SDDS_BINARY:
            f.write("SDDS file mode: SDDS_BINARY\n")
        else:
            f.write("SDDS file mode: SDDS_ASCII")

        # Display the description text if available
        if sdds_obj.description[0]:
            f.write(f"SDDS file description text: {sdds_obj.description[0]}\n")

        # Display additional description contents if available
        if sdds_obj.description[1]:
            f.write(f"SDDS file description contents: {sdds_obj.description[1]}\n")

        # Check and print parameter definitions if any are present
        if sdds_obj.parameterName:
            f.write("\nParameters:\n")
            for i, definition in enumerate(sdds_obj.parameterDefinition):
                name = sdds_obj.parameterName[i]
                datatype = sdds.sdds_data_type_to_string(definition[4])
                units = definition[1]
                description = definition[2]
                f.write(f"  {name}\n")
                f.write(f"    Datatype: {datatype}")
                if units:
                    f.write(f", Units: {units}")
                if description:
                    f.write(f", Description: {description}")
                f.write("\n")  # Newline for readability

        # Check and print array definitions if any are present
        if sdds_obj.arrayName:
            f.write("\nArrays:")
            for i, definition in enumerate(sdds_obj.arrayDefinition):
                name = sdds_obj.arrayName[i]
                datatype = sdds.sdds_data_type_to_string(definition[5])
                units = definition[1]
                description = definition[2]
                dimensions = definition[7]
                f.write(f"  {name}\n")
                f.write(f"    Datatype: {datatype}, Dimensions: {dimensions}")
                if units:
                    f.write(f", Units: {units}")
                if description:
                    f.write(f", Description: {description}")
                f.write("\n")  # Newline for readability

        # Check and print column definitions if any are present
        if sdds_obj.columnName:
            f.write("\nColumns:")
            for i, definition in enumerate(sdds_obj.columnDefinition):
                name = sdds_obj.columnName[i]
                datatype = sdds.sdds_data_type_to_string(definition[4])
                units = definition[1]
                description = definition[2]
                f.write(f"  {name}\n")
                f.write(f"    Datatype: {datatype}")
                if units:
                    f.write(f", Units: {units}")
                if description:
                    f.write(f", Description: {description}")
                f.write("\n")  # Newline for readability

        # Iterate through each loaded page and display parameter, array, and column data
        for page in range(sdds_obj.loaded_pages):
            f.write(f"\nPage: {page + 1}\n")

            # Display parameter data for the current page
            for i, name in enumerate(sdds_obj.parameterName):
                value = sdds_obj.parameterData[i][page]
                f.write(f"  Parameter '{name}': {value}\n")

            # Display array data for the current page
            for i, name in enumerate(sdds_obj.arrayName):
                value = sdds_obj.arrayData[i][page]
                f.write(f"  Array '{name}': {value}\n")

            # Display column data for the current page
            for i, name in enumerate(sdds_obj.columnName):
                value = sdds_obj.columnData[i][page]
                f.write(f"  Column '{name}': {value}\n")

    # Optionally delete the SDDS object
    del sdds_obj