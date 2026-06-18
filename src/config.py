# ─────────────────────────────────────────────────────────────
#  config.py  — Fonte única de verdade para regras de Tracy
# ─────────────────────────────────────────────────────────────

REGRAS_RAW: list[tuple[str, str, str]] = [
    # ── MAIÚSCULAS ──────────────────────────────────────────
    ('Be', 'He', "B esquerdo = H esquerdo"),
    ('Ce', 'Oe', "C esquerdo = O esquerdo"),
    ('De', 'He', "D esquerdo = H esquerdo"),
    ('Dd', 'Od', "D direito = O direito"),
    ('Ee', 'He', "E esquerdo = H esquerdo"),
    ('Fe', 'He', "F esquerdo = H esquerdo"),
    ('Ge', 'Oe', "G esquerdo = O esquerdo"),
    ('Ie', 'He', "I esquerdo = H esquerdo"),
    ('Id', 'Hd', "I direito = H direito"),
    ('Jd', 'Hd', "J direito = H direito"),
    ('Ke', 'He', "K esquerdo = H esquerdo"),
    ('Le', 'He', "L esquerdo = H esquerdo"),
    ('Md', 'Hd', "M direito = H direito"),
    ('Pe', 'He', "P esquerdo = H esquerdo"),
    ('Pd', 'Od', "P direito = O direito"),
    ('Qe', 'Oe', "Q esquerdo = O esquerdo"),
    ('Qd', 'Od', "Q direito = O direito"),
    ('Re', 'He', "R esquerdo = H esquerdo"),
    ('Ue', 'He', "U esquerdo = H esquerdo"),
    # ── MINÚSCULAS ───────────────────────────────────────────
    ('be', 'ne', "b esquerdo = n esquerdo"),
    ('bd', 'oe', "b direito = o direito"),
    ('ce', 'oe', "c esquerdo = o esquerdo"),
    ('de', 'oe', "d esquerdo = o esquerdo"),
    ('dd', 'ne', "d direito = n esquerdo"),
    ('ee', 'oe', "e esquerdo = o esquerdo"),
    ('id', 'ne', "i direito = n esquerdo"),
    ('jd', 'ne', "j direito = n esquerdo"),
    ('je', 'ne', "j esquerdo = n esquerdo"),
    ('ke', 'ne', "k esquerdo = n esquerdo"),
    ('ld', 'ne', "l direito = n esquerdo"),
    ('md', 'ne', "m direito = n esquerdo"),
    ('me', 'ne', "m esquerdo = n esquerdo"),
    ('pd', 'od', "p direito = o direito"),
    ('qe', 'oe', "q esquerdo = o esquerdo"),
    ('qd', 'ne', "q direito = n esquerdo"),
    ('re', 'ne', "r esquerdo = n esquerdo"),
    ('ue', 'nd', "u esquerdo = n direito"),
    ('ud', 'nd', "u direito = n direito"),
]

# Mapa label → (alvo, ref)
REGRAS_MAP: dict[str, tuple[str, str]] = {
    desc: (a, r)
    for a, r, desc in sorted(REGRAS_RAW, key=lambda x: (x[0].islower(), x[2]))
}