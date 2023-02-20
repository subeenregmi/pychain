x = {'txid0':

         {'7b6632fce3914fd9b098a10760a995a41dcb260a9a740b7ed6fd0902e2c47ed6'
          : ('0000', '408b22520c20af4de60e54aa2af78486e661efbffc38286253a54bcf24ab2b79934020d79daebf01adb60a15f87eec4c2f41bf5804eab89a8aa995b6224f15f5782c')
          }
     }

print(x['txid0'])

if "7b6632fce3914fd9b098a10760a995a41dcb260a9a740b7ed6fd0902e2c47ed6" in x['txid0']:
    print("YES")

if 'a' in ['bssa']:
    print(True)

if "cd1b75e9bd1d170afa45ef11a2807420080d7fe08a85bea4d7667dd6b78c3294" in ['8266deca6c65b39468e6fb8596869a231b9582ee3818d12ba7240cb126ebfb44']:
    print(True)