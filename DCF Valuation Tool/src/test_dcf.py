import unittest
from dcf_model import DCFModel

class TestDCFModel(unittest.TestCase):
    def test_basic_valuation(self):
        # Textbook example inputs
        # FCF = 100, Growth = 5%, WACC = 10%, Terminal Growth = 2%, Shares = 100
        # Years = 5
        
        model = DCFModel(
            current_fcf=100,
            growth_rate=0.05,
            wacc=0.10,
            terminal_growth_rate=0.02,
            shares_outstanding=100,
            projection_years=5
        )
        
        results = model.calculate_intrinsic_value()
        
        print("\n--- DCF Valuation Results ---")
        print(f"PV Projected: {results['pv_projected']:.2f}")
        print(f"PV Terminal:  {results['pv_terminal']:.2f}")
        print(f"Share Price:  {results['price_per_share']:.2f}")
        
        # Logic Checks
        self.assertTrue(results['price_per_share'] > 0)
        self.assertTrue(results['pv_terminal'] > results['pv_projected']) # Usually true for stable companies
        
        # Verify simple math (approximate)
        # Year 1 FCF = 105
        # PV Year 1 = 105 / 1.1 = 95.45
        self.assertAlmostEqual(results['projected_fcfs'][0], 105.0)

    def test_wacc_error_handling(self):
        # WACC <= Terminal Rate should fail
        model = DCFModel(100, 0.05, 0.02, 0.03, 100)
        with self.assertRaises(ValueError):
            model.calculate_intrinsic_value()

if __name__ == '__main__':
    unittest.main()
