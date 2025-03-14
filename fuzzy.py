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
