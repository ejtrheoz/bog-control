import numpy as np

class FermateanFuzzySet:
    """
    Represents a Fermatean Fuzzy Set (FFS) with membership (mu) and non-membership (nu) degrees.
    """
    def __init__(self, mu, nu):
        """
        Initialize a Fermatean Fuzzy Set.
        
        :param mu: Membership degree (0 <= mu <= 1)
        :param nu: Non-membership degree (0 <= nu <= 1)
        """
        if not (0 <= mu <= 1 and 0 <= nu <= 1):
            raise ValueError("Membership and non-membership degrees must be in [0, 1].")
        if mu**3 + nu**3 > 1:
            raise ValueError("Fermatean Fuzzy condition violated: mu^3 + nu^3 must be <= 1.")
        self.mu = mu
        self.nu = nu

    def score(self):
        """
        Calculate the score function for the Fermatean Fuzzy Set.
        
        :return: Score value (higher score means higher preference)
        """
        return (1 + self.mu**3 - self.nu**3) / 2

    def __str__(self):
        return f"FermateanFuzzySet(mu={self.mu}, nu={self.nu})"


class FFLDWA:
    """
    Implements the Fermatean Fuzzy Linguistic Dombi Weighted Average (FFLDWA) operator.
    """
    def __init__(self, c=3):
        """
        Initialize the FFLDWA operator.
        
        :param c: Comparative coefficient (default is 3)
        """
        self.c = c

    def aggregate(self, ffs_list, weights):
        if len(ffs_list) != len(weights):
            raise ValueError("Length of ffs_list and weights must be the same.")

        # Compute weighted sum of cubes for membership and non-membership degrees.
        mu_cube_sum = np.sum([weights[i] * (ffs_list[i].mu ** 3) for i in range(len(ffs_list))])
        nu_cube_sum = np.sum([weights[i] * (ffs_list[i].nu ** 3) for i in range(len(ffs_list))])

        # Aggregated membership and non-membership (cube-root transformation)
        mu_agg = mu_cube_sum ** (1/3)
        nu_agg = nu_cube_sum ** (1/3)

        return FermateanFuzzySet(mu_agg, nu_agg)


# Example Usage with Corrected Data
if __name__ == "__main__":
    # Step 1: Define Fermatean Fuzzy Sets with valid mu and nu values
    # Adjusted values to ensure mu^3 + nu^3 <= 1
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

    # Step 5: Output results
    print("Aggregated Fermatean Fuzzy Sets for each criterion:")
    for i, ffs in enumerate(aggregated_criteria):
        print(f"Criterion {i+1}: {ffs} (Score: {ffs.score():.4f})")