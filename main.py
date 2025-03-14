import numpy as np

# Fermatean Fuzzy Set Class
class FermateanFuzzySet:
    def __init__(self, mu, nu):
        """
        Initialize a Fermatean Fuzzy Set with membership (mu) and non-membership (nu) values.
        """
        if mu**3 + nu**3 > 1:
            raise ValueError("Invalid Fermatean Fuzzy Set: mu^3 + nu^3 must be <= 1")
        self.mu = mu
        self.nu = nu

    def score(self):
        """
        Calculate the score function for defuzzification.
        """
        return (self.mu**3 + 1 - self.nu**3) / 2

# Fermatean Fuzzy Linguistic Dombi Weighted Average (FFLDWA)
def FFLDWA(expert_weights, expert_opinions):
    """
    Aggregate expert opinions using the FFLDWA method.
    :param expert_weights: List of weights for each expert.
    :param expert_opinions: List of FermateanFuzzySet objects representing expert opinions.
    :return: Aggregated FermateanFuzzySet.
    """
    if len(expert_weights) != len(expert_opinions):
        raise ValueError("Number of expert weights must match number of expert opinions.")

    # Dombi aggregation parameters
    C = 3  # Comparative coefficient
    rho = 1.38  # Linguistic scale parameter

    # Aggregate membership and non-membership values
    aggregated_mu = 0
    aggregated_nu = 0

    for weight, opinion in zip(expert_weights, expert_opinions):
        # Calculate weighted membership and non-membership
        weighted_mu = weight * (opinion.mu**3 / (1 - opinion.mu**3))**C
        weighted_nu = weight * ((1 - opinion.nu) / opinion.nu)**C

        aggregated_mu += weighted_mu
        aggregated_nu += weighted_nu

    # Final aggregation
    aggregated_mu = 1 / (1 + aggregated_mu**(1/C))
    aggregated_nu = 1 / (1 + aggregated_nu**(1/C))

    return FermateanFuzzySet(aggregated_mu, aggregated_nu)

# Fermatean Fuzzy Stepwise Weight Assessment Ratio Analysis (FF-SWARA)
def FF_SWARA(criteria_scores):
    """
    Determine weights for criteria using the FF-SWARA method.
    :param criteria_scores: List of score function values for each criterion.
    :return: List of weights for each criterion.
    """
    # Sort criteria in descending order of scores
    sorted_indices = np.argsort(criteria_scores)[::-1]
    sorted_scores = np.array(criteria_scores)[sorted_indices]

    # Calculate comparative significance and coefficients
    c = [0]  # Comparative significance
    k = [1]  # Comparative coefficient
    q = [1]  # Recalculated weight

    for i in range(1, len(sorted_scores)):
        c_i = sorted_scores[i - 1] - sorted_scores[i]
        c.append(c_i)
        k_i = c_i + 1
        k.append(k_i)
        q_i = q[i - 1] / k_i
        q.append(q_i)

    # Calculate final weights
    total_q = sum(q)
    weights = [q_i / total_q for q_i in q]

    return weights

# Example Usage
if __name__ == "__main__":
    # Define expert weights and opinions
    expert_weights = [0.376, 0.289, 0.177, 0.157]  # Example weights
    expert_opinions = [
        FermateanFuzzySet(0.760, 0.299),  # Expert 1
        FermateanFuzzySet(0.587, 0.488),  # Expert 2
        FermateanFuzzySet(0.343, 0.721),  # Expert 3
        FermateanFuzzySet(0.299, 0.760),  # Expert 4
    ]

    # Aggregate expert opinions using FFLDWA
    aggregated_opinion = FFLDWA(expert_weights, expert_opinions)
    print(f"Aggregated Opinion (mu, nu): ({aggregated_opinion.mu:.3f}, {aggregated_opinion.nu:.3f})")
    print(f"Score: {aggregated_opinion.score():.3f}")

    # Define criteria scores for FF-SWARA
    criteria_scores = [1.547, 1.010, 0.758, 0.752, 1.305]  # Example scores
    criteria_weights = FF_SWARA(criteria_scores)
    print("Criteria Weights:", [f"{w:.3f}" for w in criteria_weights])