from DiskUsageCalculator import DiskUsageCalculator
from Filters import Filters

def main():
    directory = Filters.get_directory_input()
    extension_filter = Filters.get_extension_filter_input()
    date_filter = Filters.get_date_filter_input()
    depth_filter = Filters.get_max_depth_input()

    calculator = DiskUsageCalculator(directory)
    calculator.calculate_disk_usage(extension_filter, date_filter, depth_filter)


if __name__ == "__main__":
    main()
