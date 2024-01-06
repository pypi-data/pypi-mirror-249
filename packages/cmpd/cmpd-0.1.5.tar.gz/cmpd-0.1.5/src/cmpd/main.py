import pandas as pd 
import argparse

def main():
    print("Hello from cmpd, a compare tool!")
    parser = argparse.ArgumentParser(description='Compare tool')
    subparsers = parser.add_subparsers(dest='subcommand', help='Subcommands')

    sum_parser = subparsers.add_parser('sum', help='Calculate sum')
    sum_parser.add_argument('uoa', type=str, help='Unit of analysis')
    sum_parser.add_argument('a', type=str, help='File A')
    sum_parser.add_argument('b', type=str, help='File B')
    sum_parser.add_argument('agg', type=str, help='Aggregation column')

    set_parser = subparsers.add_parser('set', help='Compare sets')
    set_parser.add_argument('uoa', type=str, help='Unit of analysis')
    set_parser.add_argument('a', type=str, help='File A')
    set_parser.add_argument('b', type=str, help='File B')

    diff_parser = subparsers.add_parser('diff', help='Get differences')
    diff_parser.add_argument('uoa', type=str, help='Unit of analysis')
    diff_parser.add_argument('a', type=str, help='File A')
    diff_parser.add_argument('b', type=str, help='File B')

    diff_sum_parser = subparsers.add_parser('diff_sum', help='Calculate difference in sum')
    diff_sum_parser.add_argument('uoa', type=str, help='Unit of analysis')
    diff_sum_parser.add_argument('a', type=str, help='File A')
    diff_sum_parser.add_argument('b', type=str, help='File B')
    diff_sum_parser.add_argument('agg', type=str, help='Aggregation column')

    args = parser.parse_args()

    if args.subcommand == 'sum':
        result = cmpd_sum(args.uoa, args.a, args.b, args.agg)
        print(f"Sum result: {result}")
    elif args.subcommand == 'set':
        result = cmpd_set(args.uoa, args.a, args.b)
        print(f"Set result: {result}")
    elif args.subcommand == 'diff':
        result = cmpd_get_diff(args.uoa, args.a, args.b)
        print(f"Differences:\n{result}")
    elif args.subcommand == 'diff_sum':
        result = cmpd_diff_sum(args.uoa, args.a, args.b, args.agg)
        print(f"Difference in sum:\n{result}")
    else:
        parser.print_help()    

def cmpd_sum(uoa, a, b, agg):
    uoa = uoa # unit of analysis
    agg = agg
    df1 = pd.read_csv(a)
    df1g = df1.groupby(uoa)[agg].sum()
    df2 = pd.read_csv(b)
    df2g = df2.groupby(uoa)[agg].sum()
    return df1g.equals(df2g)

def cmpd_diff_sum(uoa, a, b, agg):
    uoa = uoa.split(',')
    df1 = pd.read_csv(a)
    df2 = pd.read_csv(b)
    sum_a = df1.groupby(uoa)[agg].sum()
    sum_b = df2.groupby(uoa)[agg].sum()
    variance = sum_a - sum_b
    result = pd.concat([sum_a, sum_b, variance], axis=1)
    result.columns = ['Sum of A', 'Sum of B', 'Variance']
    return result

if __name__ == "__main__":
    main()
    

def cmpd_set(uoa, a, b):
    df1 = pd.read_csv(a)
    df2 = pd.read_csv(b)
    return set(df1[uoa]) == set(df2[uoa])

def cmpd_get_diff(uoa, a, b):
    df1 = pd.read_csv(a)
    df2 = pd.read_csv(b)
    diff_a = set(df1[uoa]) - set(df2[uoa])
    diff_b = set(df2[uoa]) - set(df1[uoa])
    diff_df = pd.concat([pd.DataFrame({f'{uoa}': list(diff_a), 'Difference': 'in A not in B'}),
                        pd.DataFrame({f'{uoa}': list(diff_b), 'Difference': 'in B not in A'})])
    return diff_df.reset_index(drop=True)

if __name__ == "__main__":
    main()