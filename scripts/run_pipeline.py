"""Script principal para ejecutar preparación de datos y EDA inicial."""

from arc_project.data_prep import integrate_hyperaktiv
from arc_project.eda import compute_target_correlations, save_correlation_table


def main() -> None:
    df = integrate_hyperaktiv()
    print(f"Dataset integrado guardado: n = {len(df)} pacientes, {df.shape[1]} columnas")
    print(f"Rango ASRS: {df['ASRS'].min():.1f} - {df['ASRS'].max():.1f} "
          f"(media = {df['ASRS'].mean():.2f}, DE = {df['ASRS'].std():.2f})")

    corr_df = compute_target_correlations(df, target="ASRS")
    save_correlation_table(corr_df, top_n=50)

    print("\nTop 15 variables correlacionadas con ASRS (Pearson r):")
    print(corr_df.head(15)[["variable", "n", "r", "p_value"]].to_string(index=False))


if __name__ == "__main__":
    main()
