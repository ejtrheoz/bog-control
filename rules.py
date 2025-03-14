from fuzzy import FermateanFuzzySet, FFLDWA


class BOGReleaseRules:
    """
    Implements the rules for Boil-off Gas (BOG) release using Fermatean Fuzzy Sets and FFLDWA.
    """
    def __init__(self):
        """
        Initialize the BOG release rules.
        """
        # Define thresholds for tank pressure and risk levels
        self.safe_pressure_threshold = 0.5  # MPa (example value)
        self.warning_pressure_threshold = 0.6  # MPa (example value)
        self.high_risk_pressure_threshold = 0.7  # MPa (example value)
        self.prohibited_pressure_threshold = 0.8  # MPa (example value)

    def evaluate_release_conditions(self, tank_pressure, aggregated_risk_scores):
        """
        Evaluate whether BOG should be released based on tank pressure and aggregated risk scores.
        
        :param tank_pressure: Current pressure in the LH2 tank (MPa)
        :param aggregated_risk_scores: List of aggregated FermateanFuzzySet objects representing risk scores for each criterion.
        :return: Tuple (should_release, release_location_type)
        """
        # Step 1: Calculate the overall risk score using FFLDWA
        ffldwa = FFLDWA(c=3)
        overall_risk = ffldwa.aggregate(aggregated_risk_scores, [1/len(aggregated_risk_scores)] * len(aggregated_risk_scores))

        # Step 2: Map the overall risk score to a risk level
        risk_level = self.map_risk_level(overall_risk.score())

        # Step 3: Apply rules based on risk level and tank pressure
        if risk_level == "Prohibited":
            return False, "Prohibited location or weather condition"

        if risk_level == "High Risk":
            if tank_pressure >= self.high_risk_pressure_threshold:
                return True, "High-risk location"
            else:
                return False, "Pressure below high-risk threshold"

        if risk_level == "Warning":
            if tank_pressure >= self.warning_pressure_threshold:
                return True, "Warning location"
            else:
                return False, "Pressure below warning threshold"

        if risk_level == "Safe":
            if tank_pressure >= self.safe_pressure_threshold:
                return True, "Safe location"
            else:
                return False, "Pressure below safe threshold"

        # Default: No release
        return False, "No release conditions met"

    def map_risk_level(self, risk_score):
        """
        Map the overall risk score to a risk level.
        
        :param risk_score: Overall risk score (0 to 1)
        :return: Risk level (Safe, Warning, High Risk, Prohibited)
        """
        if risk_score >= 0.8:
            return "Prohibited"
        elif risk_score >= 0.6:
            return "High Risk"
        elif risk_score >= 0.4:
            return "Warning"
        else:
            return "Safe"
