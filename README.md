# Simularea unui Sistem Masa-Arc-Amortizor

## Descriere

Acest proiect simuleaza comportamentul dinamic al unui sistem masa-arc-amortizor (mass-spring-damper) supus unor conditii initiale, folosind integrarea numerica prin **metoda Euler**. Scopul este de a analiza cum influenteaza coeficientul de amortizare `c` raspunsul in timp al sistemului.

---

## Model Matematic

Ecuatia de miscare a unui sistem masa-arc-amortizor este:

```
m * x''(t) + c * x'(t) + k * x(t) = 0
```

unde:
- `m` - masa corpului [kg]
- `c` - coeficientul de amortizare [N*s/m]
- `k` - constanta arcului [N/m]
- `x(t)` - pozitia in functie de timp [m]
- `x'(t)` - viteza [m/s]
- `x''(t)` - acceleratia [m/s^2]

### Rescrierea ca sistem de ecuatii de ordinul 1

Pentru integrarea numerica, ecuatia de ordinul 2 se rescrie ca un sistem de doua ecuatii de ordinul 1:

```
dx/dt  =  v
dv/dt  = -(c/m) * v - (k/m) * x
```

Aceasta forma corespunde exact implementarii din `simulation.py`:
```python
dx_dt = v
dv_dt = -(c / m) * v - (k / m) * x
```

### Tipuri de amortizare

Comportamentul sistemului depinde de **factorul de amortizare** zeta (z):

```
z = c / (2 * sqrt(m * k))
```

| Conditie | Tip amortizare       | Comportament                                    |
|----------|----------------------|-------------------------------------------------|
| z < 1    | Subdampat            | Oscilatii care se sting in timp (exponential)   |
| z = 1    | Critic amortizat     | Revenire rapida la echilibru fara oscilatii     |
| z > 1    | Supradampat          | Revenire lenta la echilibru fara oscilatii      |

Amortizarea critica corespunde valorii: `c_cr = 2 * sqrt(m * k)`

---

## Parametri utilizati in simulare

Valorile de mai jos sunt exact cele definite in `main.py`:

| Parametru              | Valoare  |
|------------------------|----------|
| Masa `m`               | 1.0 kg   |
| Constanta arcului `k`  | 10.0 N/m |
| Pozitie initiala `x0`  | 1.0 m    |
| Viteza initiala `v0`   | 0.0 m/s  |
| Timp total `t_max`     | 10.0 s   |
| Pas de timp `dt`       | 0.01 s   |

**Amortizarea critica** pentru acesti parametri: `c_cr = 2 * sqrt(1.0 * 10.0) = 6.32 N*s/m`

Valorile de amortizare simulate (`damping_values = [0.2, 0.8, 5.0]` din `main.py`):

| Valoare `c` | Factor z | Tip                |
|-------------|----------|--------------------|
| 0.2         | 0.032    | Subdampat slab     |
| 0.8         | 0.126    | Subdampat moderat  |
| 5.0         | 0.790    | Subdampat puternic |

Toate trei valori sunt subdampate (z < 1) deoarece `c_cr = 6.32`, deci niciuna din valori nu o depaseste.

---

## Metoda Numerica - Metoda Euler

Metoda Euler avanseaza solutia cu un pas mic de timp `dt`:

```
x(t + dt) = x(t) + dt * v(t)
v(t + dt) = v(t) + dt * (-(c/m)*v(t) - (k/m)*x(t))
```

In `simulation.py`, numarul de pasi este calculat ca `n_steps = int(t_max / dt) + 1`, adica 1001 pasi pentru `t_max=10` si `dt=0.01`.

Este o metoda simpla de integrare explicita, potrivita pentru sisteme liniare cu pasi de timp suficient de mici.

---

## Structura Proiectului

```
TSS/
|-- main.py         # Punct de intrare; defineste parametrii si apeleaza functiile
|-- simulation.py   # Logica de simulare numerica (metoda Euler)
|-- plotting.py     # Vizualizarea rezultatelor cu matplotlib
|-- README.md       # Documentatie
```

### `simulation.py`

Contine functia `simulate_mass_spring_damper(m, c, k, x0, v0, t_max, dt)` care:
- Initializeaza vectorii `t_values`, `x_values`, `v_values` cu zerouri (`np.zeros`)
- Seteaza conditiile initiale: `x_values[0] = x0`, `v_values[0] = v0`
- Itereaza prin toti pasii de timp aplicand metoda Euler
- Returneaza vectorii `t_values`, `x_values`, `v_values`

### `plotting.py`

Contine doua functii:
- `plot_single_case(t_values, x_values, v_values)` - afiseaza pozitia si viteza pe doua subgrafice (subplot 2x1) pentru cazul `c = 0.8`
- `plot_damping_comparison(m, k, x0, v0, t_max, dt, damping_values)` - suprapune evolutiile pozitiilor pentru `c = [0.2, 0.8, 5.0]` pe acelasi grafic

### `main.py`

Apeleaza simularea si vizualizarea pentru:
1. Graficul comparativ cu `damping_values = [0.2, 0.8, 5.0]`
2. Graficul detaliat (pozitie + viteza) pentru cazul `c = 0.8`

---

## Instalare si rulare

### Cerinte

- Python 3.x
- `numpy`
- `matplotlib`

### Instalare dependente

```bash
pip install numpy matplotlib
```

### Rulare

```bash
python main.py
```

---

## Interpretarea Rezultatelor

### Grafic comparativ - cele 3 valori de amortizare

**c = 0.2 (subdampat slab, z = 0.032)**

Sistemul oscileaza aproape fara pierdere de energie. Amplitudinea scade foarte lent, iar oscilatiile persista pe toata durata simulatiei (10 s). Frecventa oscilatiilor ramane aproape constanta. Acest comportament este specific sistemelor cu amortizare neglijabila, de exemplu un pendul in vid sau un resort cu frecare minima.

**c = 0.8 (subdampat moderat, z = 0.126)**

Amplitudinea oscilatiilor descreste vizibil mai rapid fata de cazul anterior. Sistemul continua sa oscileze, dar energia se disipeaza mai eficient. Comportamentul este specific multor sisteme mecanice reale, de exemplu sisteme de suspensie usoara. Acesta este si cazul folosit in graficul detaliat (pozitie + viteza).

**c = 5.0 (subdampat puternic, z = 0.790)**

Desi sistemul ramane tehnic subdampat (z < 1), amortizarea este suficient de puternica incat oscilatiile dispar rapid. Sistemul revine la echilibru in cateva secunde, cu oscilatii abia vizibile. Se apropie de comportamentul unui sistem critic amortizat (`c_cr = 6.32`).

### Grafic detaliat - pozitie si viteza pentru c = 0.8

Graficul este generat de `plot_single_case` si contine doua subgrafice:

- **Pozitia x(t)** (subplot de sus): prezinta oscilatii sinusoidale amortizate exponential. Fiecare ciclu are o amplitudine mai mica decat precedentul. Pozitia initiala este `x0 = 1.0 m`, iar sistemul converge catre 0.
- **Viteza v(t)** (subplot de jos): este defazata cu 90 de grade fata de pozitie. Viteza este maxima cand pozitia trece prin zero si zero cand pozitia este la extrem. Amplitudinea vitezei scade si ea exponential.

### Concluzie

Simularea demonstreaza ca valoarea coeficientului de amortizare `c` controleaza rata de disipare a energiei in sistem:
- `c` mic (0.2) -> oscilatii indelungate, energie pastrata in sistem
- `c` moderat (0.8) -> oscilatii care se sting progresiv
- `c` mare (5.0) -> revenire rapida la echilibru, comportament aproape de amortizarea critica

Metoda Euler cu `dt = 0.01 s` si `n_steps = 1001` ofera rezultate corecte calitativ pentru acest sistem liniar.

---

## Autor

Proiect realizat pentru disciplina **Tehnici de Simulare a Sistemelor (TSS)**.
