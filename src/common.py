class Common:
    @staticmethod
    def get_criteria_selection(criteria_menu, prompt="Enter your choice: "):
        print("\nSearch Criteria:")
        print("****************")
        for item in criteria_menu:
            print(f" {item['option']}. {item['description']}")
        print("\n")
        try:
            choice = int(input(prompt))
            selected_criteria = next((item for item in criteria_menu if item["option"] == choice), None)
            if not selected_criteria:
                print("Invalid choice. Please try again.")
                return None
            search_value = input(f"Enter value for {selected_criteria['description']}: ")
            return selected_criteria, search_value
        except ValueError:
            print("Invalid input. Please enter a number.")
            return None

    @staticmethod
    def prepare_updates(fields_to_update):
        updates = []
        params = []
        for field, value in fields_to_update.items():
            if value:
                updates.append(f"{field} = ?")
                params.append(value)
        return updates, params
