from api import fetch_live_price
from models import Asset
from storage import load_watchlist, save_watchlist


def get_float_input(prompt):
    while True:
        try:
            input_value = input(prompt)
            return float(input_value)
        except ValueError:
            print("Invalid input. Please enter a valid price.")


def get_symbol_input():
    while True:
        input_value = input("Enter asset symbol: ").strip().upper()
        if input_value:
            return input_value
        else:
            print("Invalid input. Please enter a valid symbol.")


def get_name_input():
    while True:
        input_value = input("Enter asset name: ").strip().title()
        if input_value:
            return input_value
        else:
            print("Invalid input. Please enter a valid name.")


def display_menu():
    print("\nWatchlist Tracker Menu:")
    print("1. View Watchlist")
    print("2. Add New Asset")
    print("3. Refresh All Live Prices")
    print("4. Remove Asset")
    print("5. Exit\n")


def main():
    watchlist = load_watchlist()
    if watchlist:
        print("Syncing live prices...")
        for asset in watchlist:
            live_price = fetch_live_price(asset.symbol)
            if live_price is not None:
                asset.current_price = fetch_live_price(asset.symbol)
        save_watchlist(watchlist)

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()
        if choice == "1":
            if not watchlist:
                print("\n----------\nYour watchlist is empty.\n----------")
            else:
                print("\nYour Watchlist:")
                for asset in watchlist:
                    print(asset)
        elif choice == "2":
            symbol = get_symbol_input()
            name = get_name_input()
            target_price = get_float_input("Enter target price: ")
            print(f"Fetching live price for {symbol}...")
            live_price = fetch_live_price(symbol)
            if live_price is None:
                print("Could not verify ticker symbol. Asset was not added.")
                continue
            current_price = live_price

            existing_asset = None
            for asset in watchlist:
                if asset.symbol == symbol or asset.name == name:
                    existing_asset = asset
                    break

            if existing_asset is not None:
                existing_asset.current_price = current_price
                existing_asset.target_price = target_price
                save_watchlist(watchlist)
                print(f"Asset {symbol} ({name}) updated.")
            else:
                new_asset = Asset(symbol, name, target_price, current_price)
                watchlist.append(new_asset)
                save_watchlist(watchlist)
                print(f"Asset {symbol} added to watchlist.")

        elif choice == "3":
            if not watchlist:
                print("\n----------\nYour watchlist is empty.\n----------")
            else:
                print("\nRefreshing live prices...")
                update_counter = 0
                for asset in watchlist:
                    live_price = fetch_live_price(asset.symbol)
                    if live_price is not None:
                        asset.current_price = live_price
                        update_counter += 1
                save_watchlist(watchlist)
                print(f"Updated {update_counter} of {len(watchlist)} assets.")
        elif choice == "4":
            symbol = get_symbol_input()
            found = False
            for asset in watchlist:
                if asset.symbol == symbol:
                    watchlist.remove(asset)
                    save_watchlist(watchlist)
                    print(f"Asset {symbol} removed from watchlist.")
                    found = True
                    break
            if not found:
                print(f"Asset {symbol} not found in watchlist.")
        elif choice == "5":
            print("Exiting Watchlist Tracker. Goodbye!")
            break
        else:
            print("Invalid option. Please choose a number between 1 and 5.")


if __name__ == "__main__":
    main()
