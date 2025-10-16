import math
import argparse
import sys


def power_multiplier(size: int) -> float:
    """Calcula getPowerMultiplier() do Java:
    calc = 0.5 * (size - 5) ** 1.8
    round(calc * 100) / 100
    return max(that, 1.0)
    """
    calc = 0.5 * (size - 5) ** 1.8
    rounded = round(calc * 100) / 100.0
    return max(rounded, 1.0)


def analyze_from_power(power: int, time: int, start_power: int, sizes: list[int]):
    """Retorna cálculos quando o campo `power` da receita é conhecido."""
    results = []
    for s in sizes:
        mult = power_multiplier(s)
        if power > 0:
            gross_per_tick = power * mult
            gross_total = gross_per_tick * time
            net_total = gross_total - start_power
            net_avg_per_tick = net_total / time
        else:
            # consumidores não são multiplicados segundo o código
            gross_per_tick = power
            gross_total = gross_per_tick * time
            net_total = gross_total - start_power
            net_avg_per_tick = net_total / time

        results.append({
            "size": s,
            "multiplier": mult,
            "power_field": power,
            "time": time,
            "start_power": start_power,
            "gross_per_tick": gross_per_tick,
            "gross_total": gross_total,
            "net_total": net_total,
            "net_avg_per_tick": net_avg_per_tick,
        })
    return results


def analyze_from_desired_gross(desired_gross: float, time: int, start_power: int, sizes: list[int]):
    """Retorna cálculos quando o usuário fornece o gross per tick desejado.
    O script calcula o `power` de receita necessário para cada size:
        required_power = desired_gross / multiplier
    e mostra os totais.
    """
    results = []
    for s in sizes:
        mult = power_multiplier(s)
        # evitar divisão por zero (mult sempre >= 1.0 por implementação)
        required_power = desired_gross / mult
        # O campo power na receita é um inteiro; arredondamos para inteiro prático
        required_power_int = int(round(required_power))

        gross_per_tick = required_power_int * mult
        gross_total = gross_per_tick * time
        net_total = gross_total - start_power
        net_avg_per_tick = net_total / time

        results.append({
            "size": s,
            "multiplier": mult,
            "required_power": required_power,
            "required_power_int": required_power_int,
            "time": time,
            "start_power": start_power,
            "gross_per_tick": gross_per_tick,
            "gross_total": gross_total,
            "net_total": net_total,
            "net_avg_per_tick": net_avg_per_tick,
        })
    return results


def print_table_from_power(results: list[dict]):
    print(f"{'size':>4} | {'mult':>6} | {'power':>8} | {'gross/t':>10} | {'net_avg/t':>12} | {'gross_total':>12} | {'net_total':>12}")
    print('-' * 92)
    for r in results:
        print(f"{r['size']:4d} | {r['multiplier']:6.2f} | {r['power_field']:8d} | {r['gross_per_tick']:10.2f} | {r['net_avg_per_tick']:12.2f} | {r['gross_total']:12.0f} | {r['net_total']:12.0f}")


def print_table_from_desired(results: list[dict]):
    print(f"{'size':>4} | {'mult':>6} | {'req_power':>10} | {'req_power(int)':>14} | {'gross/t':>10} | {'net_avg/t':>12} | {'gross_total':>12} | {'net_total':>12}")
    print('-' * 120)
    for r in results:
        print(f"{r['size']:4d} | {r['multiplier']:6.2f} | {r['required_power']:10.2f} | {r['required_power_int']:14d} | {r['gross_per_tick']:10.2f} | {r['net_avg_per_tick']:12.2f} | {r['gross_total']:12.0f} | {r['net_total']:12.0f}")


def parse_sizes(sizes_input: str) -> list[int]:
    """Parseia uma string com tamanhos separados por vírgula ou um range (ex: '6,7' ou '6-12')."""
    sizes = []
    parts = [p.strip() for p in sizes_input.split(',') if p.strip()]
    for part in parts:
        if '-' in part:
            try:
                a, b = part.split('-', 1)
                start = int(a.strip())
                end = int(b.strip())
                if start <= end:
                    sizes.extend(list(range(start, end + 1)))
                else:
                    sizes.extend(list(range(end, start + 1)))
            except Exception:
                continue
        else:
            try:
                sizes.append(int(part))
            except Exception:
                continue
    # remove duplicates and sort
    return sorted(list(dict.fromkeys(sizes)))


def main():
    parser = argparse.ArgumentParser(description='Fusion reactor calculator')
    parser.add_argument('--mode', choices=['1', '2'], help='1=campo power; 2=gross per tick desejado')
    parser.add_argument('--power', type=int, help='power (E/t) do campo da receita')
    parser.add_argument('--desired', type=float, help='gross per tick desejado (E/t)')
    parser.add_argument('--time', type=int, help='time em ticks')
    parser.add_argument('--start', type=int, help='start-power (E)')
    parser.add_argument('--sizes', type=str, help='sizes separados por vírgula ou range ex: 6,7 ou 6-12')
    args, unknown = parser.parse_known_args()

    # se argumentos foram fornecidos, usa modo não interativo
    if len(sys.argv) > 1:
        try:
            mode = args.mode or '1'
            if mode == '2':
                desired = args.desired if args.desired is not None else 20000.0
                time = args.time if args.time is not None else 2048
                start_power = args.start if args.start is not None else 40000000
                sizes_input = args.sizes if args.sizes is not None else '6,7'
                sizes = parse_sizes(sizes_input)

                results = analyze_from_desired_gross(desired, time, start_power, sizes)
                print('\nResultados (calculo do campo `power` necessário por size):')
                print_table_from_desired(results)
            else:
                power = args.power if args.power is not None else 16384
                time = args.time if args.time is not None else 2048
                start_power = args.start if args.start is not None else 40000000
                sizes_input = args.sizes if args.sizes is not None else '6,7'
                sizes = parse_sizes(sizes_input)

                results = analyze_from_power(power, time, start_power, sizes)
                print('\nResultados:')
                print_table_from_power(results)
        except Exception as e:
            print('Entrada inválida (args):', e)
            return
        return

    # fallback interativo
    print('Fusion calc — escolha o modo:')
    print('1) Inserir campo `power` da receita (comportamento original)')
    print('2) Inserir gross per tick desejado (o script calcula o `power` necessário por size)')
    mode = input('Modo (1 ou 2) [1]: ') or '1'

    try:
        if mode.strip() == '2':
            desired = float(input('gross per tick desejado (E/t) [ex: 20000]: ') or '20000')
            time = int(input('time (ticks) [ex: 2048]: ') or '2048')
            start_power = int(input('start-power (E) [ex: 40000000]: ') or '40000000')
            sizes_input = input('sizes separados por vírgula [ex: 6,7,8] (ou range 6-12): ') or '6,7'
            sizes = parse_sizes(sizes_input)

            results = analyze_from_desired_gross(desired, time, start_power, sizes)
            print('\nResultados (calculo do campo `power` necessário por size):')
            print_table_from_desired(results)
        else:
            power = int(input('power (E/t) [ex: 16384]: ') or '16384')
            time = int(input('time (ticks) [ex: 2048]: ') or '2048')
            start_power = int(input('start-power (E) [ex: 40000000]: ') or '40000000')
            sizes_input = input('sizes separados por vírgula [ex: 6,7,8] (ou range 6-12): ') or '6,7'
            sizes = parse_sizes(sizes_input)

            results = analyze_from_power(power, time, start_power, sizes)
            print('\nResultados:')
            print_table_from_power(results)
    except Exception as e:
        print('Entrada inválida:', e)
        return


if __name__ == '__main__':
    main()

