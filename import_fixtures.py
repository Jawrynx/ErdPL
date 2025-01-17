import os
import django
import pandas as pd

# Initialize Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ErdPL.settings')
django.setup()

from teams.models import Team, Division
from fixtures.models import Fixture

def import_fixtures_from_csv(csv_file_path):
    """
    Imports fixture data from a CSV file.

    Args:
        csv_file_path: Path to the CSV file.

    Assumes the CSV file has no header row and the following order:
        - Home Team
        - Away Team
        - Match Date (YYYY-MM-DD format)
        - Division
    """

    try:
        df = pd.read_csv(csv_file_path, header=None, names=['Home Team', 'Away Team', 'Match Date', 'Division'])
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return False

    for index, row in df.iterrows():
        try:
            home_team_name = row['Home Team'].strip()
            away_team_name = row['Away Team'].strip()
            match_date_str = row['Match Date'].strip()  # Remove leading/trailing whitespace
            division_name = row['Division'].strip()

            # Check if date format is valid (YYYY-MM-DD)
            try:
                pd.to_datetime(match_date_str, format='%Y-%m-%d')
            except ValueError:
                print(f"Error processing row {index+1}: Invalid date format ({match_date_str})")
                continue

            # Get or create Division
            division, _ = Division.objects.get_or_create(name=division_name)

            # Get or create Teams (ensure teams exist)
            home_team, _ = Team.objects.get_or_create(name=home_team_name)
            away_team, _ = Team.objects.get_or_create(name=away_team_name)

            # Create Fixture object
            fixture = Fixture(
                home_team=home_team.name,
                away_team=away_team.name,
                date=pd.to_datetime(match_date_str).date(),
                division=division
            )
            fixture.save()

        except Exception as e:
            print(f"Error processing row {index+1}: {e}")
            return False  # Stop processing if an error occurs

    return True

if __name__ == "__main__":
    csv_file_path = 'fixtures.csv'  # Adjust path as needed
    success = import_fixtures_from_csv(csv_file_path)

    if success:
        print("Fixture data imported successfully.")
    else:
        print("Error importing fixtures.")