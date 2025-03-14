# Import necessary modules
from fuzzy import FermateanFuzzySet, FFLDWA
from rules import BOGReleaseRules
from data_gathering import DataGatheringModule
import argparse


def rules_with_fuzzy():
    expert1 = [
        FermateanFuzzySet(mu=0.9, nu=0.1),  # Population Density
        FermateanFuzzySet(mu=0.8, nu=0.2),  # Road Type
        FermateanFuzzySet(mu=0.7, nu=0.3),  # Weather
        FermateanFuzzySet(mu=0.6, nu=0.4),  # Driving Time
        FermateanFuzzySet(mu=0.5, nu=0.5)   # Site Type
    ]
    expert2 = [
        FermateanFuzzySet(mu=0.85, nu=0.15),
        FermateanFuzzySet(mu=0.75, nu=0.25),
        FermateanFuzzySet(mu=0.65, nu=0.35),
        FermateanFuzzySet(mu=0.55, nu=0.45),
        FermateanFuzzySet(mu=0.45, nu=0.55)
    ]
    expert3 = [
        FermateanFuzzySet(mu=0.95, nu=0.05),
        FermateanFuzzySet(mu=0.85, nu=0.15),
        FermateanFuzzySet(mu=0.75, nu=0.25),
        FermateanFuzzySet(mu=0.65, nu=0.35),
        FermateanFuzzySet(mu=0.55, nu=0.45)
    ]
    expert4 = [
        FermateanFuzzySet(mu=0.9, nu=0.1),
        FermateanFuzzySet(mu=0.8, nu=0.2),
        FermateanFuzzySet(mu=0.7, nu=0.3),
        FermateanFuzzySet(mu=0.6, nu=0.4),
        FermateanFuzzySet(mu=0.5, nu=0.5)
    ]

    # Step 2: Define expert weights from the article
    expert_weights = [0.376, 0.289, 0.177, 0.157]  # Expert 1, Expert 2, Expert 3, Expert 4

    # Step 3: Initialize FFLDWA operator
    ffldwa = FFLDWA(c=3)

    # Step 4: Aggregate expert evaluations for each criterion
    aggregated_criteria = []
    for i in range(5):  # 5 criteria
        aggregated_criteria.append(ffldwa.aggregate(
            [expert1[i], expert2[i], expert3[i], expert4[i]],  # Expert evaluations for criterion i
            expert_weights  # Expert weights
        ))

    # Step 5: Initialize BOG release rules
    bog_rules = BOGReleaseRules()

    # Step 6: Evaluate release conditions
    tank_pressure = 0.65  # Example tank pressure (MPa)
    should_release, reason = bog_rules.evaluate_release_conditions(tank_pressure, aggregated_criteria)

    # Step 7: Output results
    print("Aggregated Fermatean Fuzzy Sets for each criterion:")
    for i, ffs in enumerate(aggregated_criteria):
        print(f"Criterion {i+1}: {ffs} (Score: {ffs.score():.4f})")

    print(f"\nShould release BOG: {should_release}, Reason: {reason}")


def rule_with_fuzzy_and_received_data():
    data_gatherer = DataGatheringModule()
    ffldwa = FFLDWA(c=3)
    bog_rules = BOGReleaseRules()

    # Example location (latitude and longitude)
    latitude = 34.0522  # Example: Los Angeles
    longitude = -118.2437

    # Step 1: Gather data
    population_density = data_gatherer.get_population_density(latitude, longitude)
    road_type = data_gatherer.get_road_type(latitude, longitude)
    weather_condition = data_gatherer.get_weather_condition(latitude, longitude)
    driving_time = data_gatherer.get_driving_time()
    site_type = data_gatherer.get_site_type(latitude, longitude)

    # Step 2: Map gathered data to Fermatean Fuzzy Sets
    # Example mapping rules (adjust based on your specific requirements)
    ffs_population = FermateanFuzzySet(
        mu=min(population_density / 5000, 1),  # Normalize population density (max 5000 people/km²)
        nu=0.1  # Non-membership degree (example value)
    )
    ffs_road = FermateanFuzzySet(
        mu=0.9 if road_type == "expressway" else 0.5,  # Higher membership for expressways
        nu=0.2  # Non-membership degree (example value)
    )
    ffs_weather = FermateanFuzzySet(
        mu=0.9 if weather_condition == "sunny" else 0.5,  # Higher membership for sunny weather
        nu=0.1  # Non-membership degree (example value)
    )
    ffs_time = FermateanFuzzySet(
        mu=0.8 if driving_time == "daytime" else 0.3,  # Higher membership for daytime
        nu=0.2  # Non-membership degree (example value)
    )
    ffs_site = FermateanFuzzySet(
        mu=0.9 if site_type == "urban" else 0.5,  # Higher membership for urban areas
        nu=0.2  # Non-membership degree (example value)
    )

    # Step 3: Aggregate criteria using FFLDWA
    aggregated_criteria = [ffs_population, ffs_road, ffs_weather, ffs_time, ffs_site]
    weights = [0.2, 0.2, 0.2, 0.2, 0.2]  # Equal weights for simplicity
    overall_risk = ffldwa.aggregate(aggregated_criteria, weights)

    # Step 4: Evaluate BOG release conditions
    tank_pressure = 0.65  # Example tank pressure (MPa)
    should_release, reason = bog_rules.evaluate_release_conditions(tank_pressure, aggregated_criteria)

    # Step 5: Output results
    print("Gathered Data:")
    print(f"Population Density: {population_density} people/km²")
    print(f"Road Type: {road_type}")
    print(f"Weather Condition: {weather_condition}")
    print(f"Driving Time: {driving_time}")
    print(f"Site Type: {site_type}")

    print("\nAggregated Fermatean Fuzzy Sets for each criterion:")
    for i, ffs in enumerate(aggregated_criteria):
        print(f"Criterion {i+1}: {ffs} (Score: {ffs.score():.4f})")

    print(f"\nOverall Risk Score: {overall_risk.score():.4f}")
    print(f"Should release BOG: {should_release}, Reason: {reason}")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run fuzzy evaluation modules.")
    parser.add_argument('--mode', choices=['experts', 'data'], default='experts',
                        help="Choose 'experts' to run expert fuzzy rules or 'data' to run fuzzy and received data rules.")
    args = parser.parse_args()

    if args.mode == "data":
        rule_with_fuzzy_and_received_data()
    else:
        rules_with_fuzzy()