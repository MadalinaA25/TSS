import unittest
import math
from simulation import simulate_mass_spring_damper, MassSpringDamper


# =============================================================================
# TESTE PENTRU FUNCTIA simulate_mass_spring_damper
# =============================================================================

class TestSimulateMassSpringDamperFunction(unittest.TestCase):
    """Teste de baza pentru functia standalone simulate_mass_spring_damper."""

    def test_output_length(self):
        t, x, v = simulate_mass_spring_damper(1.0, 0.8, 10.0, 1.0, 0.0, 10.0, 0.01)
        expected = int(10.0 / 0.01) + 1  # 1001
        self.assertEqual(len(t), expected)
        self.assertEqual(len(x), expected)
        self.assertEqual(len(v), expected)

    def test_initial_conditions(self):
        t, x, v = simulate_mass_spring_damper(1.0, 0.8, 10.0, 1.0, 0.0, 10.0, 0.01)
        self.assertEqual(x[0], 1.0)
        self.assertEqual(v[0], 0.0)
        self.assertEqual(t[0], 0.0)

    def test_time_vector_end(self):
        t, x, v = simulate_mass_spring_damper(1.0, 0.8, 10.0, 1.0, 0.0, 10.0, 0.01)
        self.assertAlmostEqual(t[-1], 10.0, places=5)

    def test_returns_three_arrays(self):
        result = simulate_mass_spring_damper(1.0, 0.8, 10.0, 1.0, 0.0, 10.0, 0.01)
        self.assertEqual(len(result), 3)


# =============================================================================
# 1. PARTITIONARE IN CLASE DE ECHIVALENTA
# =============================================================================
# Clase valide (CV):
#   CV1: m > 0
#   CV2: c >= 0
#   CV3: k > 0
#   CV4: t_max > 0
#   CV5: dt > 0 si dt < t_max
#
# Clase invalide (CI):
#   CI1: m <= 0
#   CI2: c < 0
#   CI3: k <= 0
#   CI4: t_max <= 0
#   CI5: dt <= 0
#   CI6: dt >= t_max
# =============================================================================

class TestEchivalenta(unittest.TestCase):

    # CV1, CV2, CV3: parametri valizi pentru __init__
    def test_CE_valid_parameters(self):
        sys = MassSpringDamper(m=1.0, c=0.8, k=10.0)
        self.assertEqual(sys.m, 1.0)
        self.assertEqual(sys.c, 0.8)
        self.assertEqual(sys.k, 10.0)

    # CV2: c = 0 este valid (sistem neamortizat)
    def test_CE_c_zero_valid(self):
        sys = MassSpringDamper(m=1.0, c=0.0, k=10.0)
        self.assertEqual(sys.c, 0.0)

    # CV4, CV5: simulate cu parametri valizi
    def test_CE_simulate_valid(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        t, x, v = sys.simulate(1.0, 0.0, t_max=10.0, dt=0.01)
        self.assertIsNotNone(t)

    # CI1: m negativ
    def test_CI_m_negative(self):
        with self.assertRaises(ValueError):
            MassSpringDamper(m=-1.0, c=0.8, k=10.0)

    # CI1: m = 0
    def test_CI_m_zero(self):
        with self.assertRaises(ValueError):
            MassSpringDamper(m=0.0, c=0.8, k=10.0)

    # CI2: c negativ
    def test_CI_c_negative(self):
        with self.assertRaises(ValueError):
            MassSpringDamper(m=1.0, c=-1.0, k=10.0)

    # CI3: k negativ
    def test_CI_k_negative(self):
        with self.assertRaises(ValueError):
            MassSpringDamper(m=1.0, c=0.8, k=-1.0)

    # CI3: k = 0
    def test_CI_k_zero(self):
        with self.assertRaises(ValueError):
            MassSpringDamper(m=1.0, c=0.8, k=0.0)

    # CI4: t_max = 0
    def test_CI_t_max_zero(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        with self.assertRaises(ValueError):
            sys.simulate(1.0, 0.0, t_max=0.0, dt=0.01)

    # CI4: t_max negativ
    def test_CI_t_max_negative(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        with self.assertRaises(ValueError):
            sys.simulate(1.0, 0.0, t_max=-5.0, dt=0.01)

    # CI5: dt = 0
    def test_CI_dt_zero(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        with self.assertRaises(ValueError):
            sys.simulate(1.0, 0.0, t_max=10.0, dt=0.0)

    # CI5: dt negativ
    def test_CI_dt_negative(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        with self.assertRaises(ValueError):
            sys.simulate(1.0, 0.0, t_max=10.0, dt=-0.01)

    # CI6: dt = t_max
    def test_CI_dt_equal_t_max(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        with self.assertRaises(ValueError):
            sys.simulate(1.0, 0.0, t_max=10.0, dt=10.0)

    # CI6: dt > t_max
    def test_CI_dt_greater_than_t_max(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        with self.assertRaises(ValueError):
            sys.simulate(1.0, 0.0, t_max=10.0, dt=20.0)


# =============================================================================
# 2. ANALIZA VALORILOR DE FRONTIERA
# =============================================================================

class TestValoriFrontiera(unittest.TestCase):

    # Frontiera m: 0 invalid, 0.001 valid
    def test_BVA_m_zero_invalid(self):
        with self.assertRaises(ValueError):
            MassSpringDamper(m=0.0, c=0.8, k=10.0)

    def test_BVA_m_very_small_valid(self):
        sys = MassSpringDamper(m=0.001, c=0.8, k=10.0)
        self.assertEqual(sys.m, 0.001)

    # Frontiera c: 0 valid, -0.001 invalid
    def test_BVA_c_zero_valid(self):
        sys = MassSpringDamper(m=1.0, c=0.0, k=10.0)
        self.assertEqual(sys.c, 0.0)

    def test_BVA_c_just_below_zero_invalid(self):
        with self.assertRaises(ValueError):
            MassSpringDamper(m=1.0, c=-0.001, k=10.0)

    # Frontiera k: 0 invalid, 0.001 valid
    def test_BVA_k_zero_invalid(self):
        with self.assertRaises(ValueError):
            MassSpringDamper(m=1.0, c=0.8, k=0.0)

    def test_BVA_k_very_small_valid(self):
        sys = MassSpringDamper(m=1.0, c=0.8, k=0.001)
        self.assertEqual(sys.k, 0.001)

    # Frontiera dt vs t_max: dt = t_max invalid, dt < t_max valid
    def test_BVA_dt_equal_t_max_invalid(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        with self.assertRaises(ValueError):
            sys.simulate(1.0, 0.0, t_max=1.0, dt=1.0)

    def test_BVA_dt_just_below_t_max_valid(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        t, x, v = sys.simulate(1.0, 0.0, t_max=1.0, dt=0.5)
        self.assertIsNotNone(t)

    # Frontiera zeta = 1 (critic)
    def test_BVA_zeta_equals_one(self):
        # m=1, k=1, c=2 → zeta = 2/(2*sqrt(1)) = 1.0
        sys = MassSpringDamper(m=1.0, c=2.0, k=1.0)
        self.assertEqual(sys.get_damping_type(), "critic")

    def test_BVA_zeta_just_below_one(self):
        # c=1.99 → zeta < 1
        sys = MassSpringDamper(m=1.0, c=1.99, k=1.0)
        self.assertEqual(sys.get_damping_type(), "subdampat")

    def test_BVA_zeta_just_above_one(self):
        # c=2.01 → zeta > 1
        sys = MassSpringDamper(m=1.0, c=2.01, k=1.0)
        self.assertEqual(sys.get_damping_type(), "supradampat")


# =============================================================================
# 3. ACOPERIRE LA NIVEL DE INSTRUCTIUNE (Statement Coverage)
# Toate liniile din __init__, simulate si get_damping_type sunt executate
# prin combinatia testelor de mai jos (acoperire 100%).
# =============================================================================

class TestAcoperiреInstructiuni(unittest.TestCase):

    def test_SC_all_init_lines(self):
        # Parcurge toate ramurile din __init__: m invalid, c invalid, k invalid, valid
        with self.assertRaises(ValueError):
            MassSpringDamper(m=0.0, c=0.8, k=10.0)
        with self.assertRaises(ValueError):
            MassSpringDamper(m=1.0, c=-1.0, k=10.0)
        with self.assertRaises(ValueError):
            MassSpringDamper(m=1.0, c=0.8, k=0.0)
        sys = MassSpringDamper(m=1.0, c=0.8, k=10.0)
        self.assertIsNotNone(sys)

    def test_SC_all_simulate_lines(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        with self.assertRaises(ValueError):
            sys.simulate(1.0, 0.0, t_max=0.0, dt=0.01)
        with self.assertRaises(ValueError):
            sys.simulate(1.0, 0.0, t_max=10.0, dt=0.0)
        with self.assertRaises(ValueError):
            sys.simulate(1.0, 0.0, t_max=10.0, dt=10.0)
        t, x, v = sys.simulate(1.0, 0.0, t_max=10.0, dt=0.01)
        self.assertIsNotNone(t)

    def test_SC_all_damping_type_lines(self):
        # Parcurge toate cele 3 ramuri din get_damping_type
        sys1 = MassSpringDamper(1.0, 0.8, 10.0)
        self.assertEqual(sys1.get_damping_type(), "subdampat")
        sys2 = MassSpringDamper(1.0, 2.0, 1.0)
        self.assertEqual(sys2.get_damping_type(), "critic")
        sys3 = MassSpringDamper(1.0, 10.0, 10.0)
        self.assertEqual(sys3.get_damping_type(), "supradampat")


# =============================================================================
# 4. ACOPERIRE LA NIVEL DE DECIZIE (Decision Coverage)
# Fiecare ramura if/else: executata cu True si cu False.
#
# __init__:  D1(m<=0), D2(c<0), D3(k<=0)
# simulate:  D4(t_max<=0), D5(dt<=0), D6(dt>=t_max)
# get_damping_type: D7(zeta<1), D8(zeta==1)
# =============================================================================

class TestAcoperireDecizii(unittest.TestCase):

    # D1 = True
    def test_DC_D1_true(self):
        with self.assertRaises(ValueError):
            MassSpringDamper(m=0.0, c=0.8, k=10.0)

    # D1 = False, D2 = True
    def test_DC_D2_true(self):
        with self.assertRaises(ValueError):
            MassSpringDamper(m=1.0, c=-1.0, k=10.0)

    # D1 = False, D2 = False, D3 = True
    def test_DC_D3_true(self):
        with self.assertRaises(ValueError):
            MassSpringDamper(m=1.0, c=0.8, k=0.0)

    # D1 = False, D2 = False, D3 = False
    def test_DC_D1_D2_D3_false(self):
        sys = MassSpringDamper(m=1.0, c=0.8, k=10.0)
        self.assertIsNotNone(sys)

    # D4 = True
    def test_DC_D4_true(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        with self.assertRaises(ValueError):
            sys.simulate(1.0, 0.0, t_max=0.0, dt=0.01)

    # D4 = False, D5 = True
    def test_DC_D5_true(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        with self.assertRaises(ValueError):
            sys.simulate(1.0, 0.0, t_max=10.0, dt=0.0)

    # D4 = False, D5 = False, D6 = True
    def test_DC_D6_true(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        with self.assertRaises(ValueError):
            sys.simulate(1.0, 0.0, t_max=10.0, dt=10.0)

    # D4 = False, D5 = False, D6 = False
    def test_DC_D4_D5_D6_false(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        t, x, v = sys.simulate(1.0, 0.0, t_max=10.0, dt=0.01)
        self.assertIsNotNone(t)

    # D7 = True: zeta < 1
    def test_DC_D7_true(self):
        sys = MassSpringDamper(m=1.0, c=0.8, k=10.0)
        self.assertEqual(sys.get_damping_type(), "subdampat")

    # D7 = False, D8 = True: zeta == 1
    def test_DC_D8_true(self):
        sys = MassSpringDamper(m=1.0, c=2.0, k=1.0)
        self.assertEqual(sys.get_damping_type(), "critic")

    # D7 = False, D8 = False (else): zeta > 1
    def test_DC_D7_D8_false(self):
        sys = MassSpringDamper(m=1.0, c=10.0, k=10.0)
        self.assertEqual(sys.get_damping_type(), "supradampat")


# =============================================================================
# 5. ACOPERIRE LA NIVEL DE CONDITIE (Condition Coverage)
# Fiecare conditie atomica ia valoarea True si False independent.
# =============================================================================

class TestAcoperireConditii(unittest.TestCase):

    # C1 (m <= 0): True
    def test_CC_C1_true(self):
        with self.assertRaises(ValueError):
            MassSpringDamper(m=-5.0, c=0.8, k=10.0)

    # C1 (m <= 0): False
    def test_CC_C1_false(self):
        sys = MassSpringDamper(m=2.0, c=0.8, k=10.0)
        self.assertGreater(sys.m, 0)

    # C2 (c < 0): True
    def test_CC_C2_true(self):
        with self.assertRaises(ValueError):
            MassSpringDamper(m=1.0, c=-3.0, k=10.0)

    # C2 (c < 0): False
    def test_CC_C2_false(self):
        sys = MassSpringDamper(m=1.0, c=0.0, k=10.0)
        self.assertGreaterEqual(sys.c, 0)

    # C3 (k <= 0): True
    def test_CC_C3_true(self):
        with self.assertRaises(ValueError):
            MassSpringDamper(m=1.0, c=0.8, k=-2.0)

    # C3 (k <= 0): False
    def test_CC_C3_false(self):
        sys = MassSpringDamper(m=1.0, c=0.8, k=5.0)
        self.assertGreater(sys.k, 0)

    # C4 (t_max <= 0): True
    def test_CC_C4_true(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        with self.assertRaises(ValueError):
            sys.simulate(1.0, 0.0, t_max=-1.0, dt=0.01)

    # C4 (t_max <= 0): False
    def test_CC_C4_false(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        t, x, v = sys.simulate(1.0, 0.0, t_max=5.0, dt=0.01)
        self.assertIsNotNone(t)

    # C5 (dt <= 0): True
    def test_CC_C5_true(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        with self.assertRaises(ValueError):
            sys.simulate(1.0, 0.0, t_max=10.0, dt=-0.5)

    # C5 (dt <= 0): False
    def test_CC_C5_false(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        t, x, v = sys.simulate(1.0, 0.0, t_max=10.0, dt=0.1)
        self.assertIsNotNone(t)

    # C6 (dt >= t_max): True
    def test_CC_C6_true(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        with self.assertRaises(ValueError):
            sys.simulate(1.0, 0.0, t_max=5.0, dt=5.0)

    # C6 (dt >= t_max): False
    def test_CC_C6_false(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        t, x, v = sys.simulate(1.0, 0.0, t_max=10.0, dt=0.01)
        self.assertIsNotNone(t)

    # C7 (zeta < 1): True
    def test_CC_C7_true(self):
        sys = MassSpringDamper(m=1.0, c=0.5, k=10.0)
        self.assertEqual(sys.get_damping_type(), "subdampat")

    # C7 (zeta < 1): False, C8 (zeta == 1): True
    def test_CC_C7_false_C8_true(self):
        sys = MassSpringDamper(m=1.0, c=2.0, k=1.0)
        self.assertEqual(sys.get_damping_type(), "critic")

    # C7 (zeta < 1): False, C8 (zeta == 1): False
    def test_CC_C7_false_C8_false(self):
        sys = MassSpringDamper(m=1.0, c=10.0, k=10.0)
        self.assertEqual(sys.get_damping_type(), "supradampat")


# =============================================================================
# 6. CIRCUITE INDEPENDENTE (Complexitate McCabe)
#
# __init__: V(G) = 3 + 1 = 4 → 4 cai independente
#   Calea 1: m<=0 → ValueError
#   Calea 2: m>0, c<0 → ValueError
#   Calea 3: m>0, c>=0, k<=0 → ValueError
#   Calea 4: m>0, c>=0, k>0 → obiect creat cu succes
#
# simulate: V(G) = 3 + 1 = 4 → 4 cai independente
#   Calea 1: t_max<=0 → ValueError
#   Calea 2: t_max>0, dt<=0 → ValueError
#   Calea 3: t_max>0, dt>0, dt>=t_max → ValueError
#   Calea 4: toti parametri valizi → simulare reusita
#
# get_damping_type: V(G) = 2 + 1 = 3 → 3 cai independente
#   Calea 1: zeta < 1 → "subdampat"
#   Calea 2: zeta == 1 → "critic"
#   Calea 3: zeta > 1 → "supradampat"
# =============================================================================

class TestCircuiteIndependente(unittest.TestCase):

    # __init__ Calea 1
    def test_IC_init_path1(self):
        with self.assertRaises(ValueError):
            MassSpringDamper(m=0.0, c=0.8, k=10.0)

    # __init__ Calea 2
    def test_IC_init_path2(self):
        with self.assertRaises(ValueError):
            MassSpringDamper(m=1.0, c=-2.0, k=10.0)

    # __init__ Calea 3
    def test_IC_init_path3(self):
        with self.assertRaises(ValueError):
            MassSpringDamper(m=1.0, c=0.8, k=0.0)

    # __init__ Calea 4
    def test_IC_init_path4(self):
        sys = MassSpringDamper(m=1.0, c=0.8, k=10.0)
        self.assertEqual(sys.m, 1.0)
        self.assertEqual(sys.c, 0.8)
        self.assertEqual(sys.k, 10.0)

    # simulate Calea 1
    def test_IC_simulate_path1(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        with self.assertRaises(ValueError):
            sys.simulate(1.0, 0.0, t_max=0.0, dt=0.01)

    # simulate Calea 2
    def test_IC_simulate_path2(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        with self.assertRaises(ValueError):
            sys.simulate(1.0, 0.0, t_max=10.0, dt=0.0)

    # simulate Calea 3
    def test_IC_simulate_path3(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        with self.assertRaises(ValueError):
            sys.simulate(1.0, 0.0, t_max=5.0, dt=5.0)

    # simulate Calea 4
    def test_IC_simulate_path4(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        t, x, v = sys.simulate(1.0, 0.0, 10.0, 0.01)
        self.assertEqual(len(t), 1001)

    # get_damping_type Calea 1: zeta < 1
    def test_IC_damping_path1(self):
        sys = MassSpringDamper(m=1.0, c=0.8, k=10.0)
        self.assertEqual(sys.get_damping_type(), "subdampat")

    # get_damping_type Calea 2: zeta == 1
    def test_IC_damping_path2(self):
        # m=1, k=1, c=2 → zeta = 2/(2*sqrt(1)) = 1.0
        sys = MassSpringDamper(m=1.0, c=2.0, k=1.0)
        self.assertEqual(sys.get_damping_type(), "critic")

    # get_damping_type Calea 3: zeta > 1
    def test_IC_damping_path3(self):
        # m=1, k=10, c=10 → zeta = 10/(2*sqrt(10)) ≈ 1.58 > 1
        sys = MassSpringDamper(m=1.0, c=10.0, k=10.0)
        self.assertEqual(sys.get_damping_type(), "supradampat")


# =============================================================================
# 7. TESTE PENTRU MUTANTI
# Teste proiectate sa omoare mutanti specifici (operatori modificati).
#
# M1: m <= 0  →  m < 0   (frontiera 0 exclusa)
# M2: c < 0   →  c <= 0  (frontiera 0 exclusa)
# M3: k <= 0  →  k < 0   (frontiera 0 exclusa)
# M4: t_max <= 0  →  t_max < 0  (frontiera 0 exclusa)
# M5: dt <= 0  →  dt < 0  (frontiera 0 exclusa)
# M6: dt >= t_max  →  dt > t_max  (frontiera exclusa)
# M7: zeta < 1  →  zeta <= 1  (modifica comportamentul la frontiera)
# M8: zeta == 1  →  zeta != 1  (neaga conditia)
# =============================================================================

class TestMutanti(unittest.TestCase):

    # Test M1: m=0 trebuie sa ridice ValueError
    # Mutantul (m < 0) ar lasa m=0 sa treaca → testul ar detecta mutantul
    def test_M1_m_zero_must_raise(self):
        with self.assertRaises(ValueError):
            MassSpringDamper(m=0.0, c=0.8, k=10.0)

    # Test M2: c=0 NU trebuie sa ridice ValueError
    # Mutantul (c <= 0) ar bloca c=0 → testul ar detecta mutantul
    def test_M2_c_zero_must_not_raise(self):
        try:
            sys = MassSpringDamper(m=1.0, c=0.0, k=10.0)
            self.assertEqual(sys.c, 0.0)
        except ValueError:
            self.fail("c=0 este valid, nu trebuie sa ridice ValueError")

    # Test M3: k=0 trebuie sa ridice ValueError
    # Mutantul (k < 0) ar lasa k=0 sa treaca → testul ar detecta mutantul
    def test_M3_k_zero_must_raise(self):
        with self.assertRaises(ValueError):
            MassSpringDamper(m=1.0, c=0.8, k=0.0)

    # Test M4: t_max=0 trebuie sa ridice ValueError
    # Mutantul (t_max < 0) ar lasa t_max=0 sa treaca → testul ar detecta mutantul
    def test_M4_t_max_zero_must_raise(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        with self.assertRaises(ValueError):
            sys.simulate(1.0, 0.0, t_max=0.0, dt=0.01)

    # Test M5: dt=0 trebuie sa ridice ValueError
    # Mutantul (dt < 0) ar lasa dt=0 sa treaca → testul ar detecta mutantul
    def test_M5_dt_zero_must_raise(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        with self.assertRaises(ValueError):
            sys.simulate(1.0, 0.0, t_max=10.0, dt=0.0)

    # Test M6: dt=t_max trebuie sa ridice ValueError
    # Mutantul (dt > t_max) ar lasa dt=t_max sa treaca → testul ar detecta mutantul
    def test_M6_dt_equal_t_max_must_raise(self):
        sys = MassSpringDamper(1.0, 0.8, 10.0)
        with self.assertRaises(ValueError):
            sys.simulate(1.0, 0.0, t_max=10.0, dt=10.0)

    # Test M7: zeta=1 trebuie sa returneze "critic", nu "subdampat"
    # Mutantul (zeta <= 1) ar returna "subdampat" pentru zeta=1 → testul ar detecta mutantul
    def test_M7_zeta_eq_1_must_be_critic_not_subdampat(self):
        sys = MassSpringDamper(m=1.0, c=2.0, k=1.0)
        result = sys.get_damping_type()
        self.assertEqual(result, "critic")
        self.assertNotEqual(result, "subdampat")

    # Test M8: zeta>1 trebuie sa returneze "supradampat", nu "critic"
    # Mutantul (zeta != 1) ar returna "critic" pentru zeta>1 → testul ar detecta mutantul
    def test_M8_zeta_gt_1_must_be_supradampat_not_critic(self):
        sys = MassSpringDamper(m=1.0, c=10.0, k=10.0)
        result = sys.get_damping_type()
        self.assertEqual(result, "supradampat")
        self.assertNotEqual(result, "critic")


if __name__ == "__main__":
    unittest.main()

