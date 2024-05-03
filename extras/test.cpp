#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <numeric>
#include <unordered_map>
#include <vector>

using u64 = uint64_t;
using u128 = __uint128_t;

u64 binpower(u64 base, u64 e, u64 mod) {
  u64 result = 1;
  base %= mod;
  while (e) {
    if (e & 1)
      result = (u128)result * base % mod;
    base = (u128)base * base % mod;
    e >>= 1;
  }
  return result;
}

bool check_composite(u64 n, u64 a, u64 d, int s) {
  u64 x = binpower(a, d, n);
  if (x == 1 || x == n - 1)
    return false;
  for (int r = 1; r < s; r++) {
    x = (u128)x * x % n;
    if (x == n - 1)
      return false;
  }
  return true;
};

bool MillerRabin(u64 n) { // returns true if n is prime, else returns false.
  if (n < 2)
    return false;

  int r = 0;
  u64 d = n - 1;
  while ((d & 1) == 0) {
    d >>= 1;
    r++;
  }

  for (int a : {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37}) {
    if (n == a)
      return true;
    if (check_composite(n, a, d, r))
      return false;
  }
  return true;
}

long long mult(long long a, long long b, long long mod) {
  long long result = 0;
  while (b) {
    if (b & 1)
      result = (result + a) % mod;
    a = (a + a) % mod;
    b >>= 1;
  }
  return result;
}

long long f(long long x, long long c, long long mod) {
  return (mult(x, x, mod) + c) % mod;
}

long long brent(long long n, long long x0 = 2, long long c = 1) {
  long long x = x0;
  long long g = 1;
  long long q = 1;
  long long xs, y;

  int m = 128;
  int l = 1;
  while (g == 1) {
    y = x;
    for (int i = 1; i < l; i++)
      x = f(x, c, n);
    int k = 0;
    while (k < l && g == 1) {
      xs = x;
      for (int i = 0; i < m && i < l - k; i++) {
        x = f(x, c, n);
        q = mult(q, std::abs(y - x), n);
      }
      g = std::gcd(q, n);
      k += m;
    }
    l *= 2;
  }
  if (g == n) {
    do {
      xs = f(xs, c, n);
      g = std::gcd(std::abs(xs - y), n);
    } while (g == 1);
  }
  return g;
}

uint64_t brent_pollard_factor(uint64_t n) {
  const uint64_t m = 1000;
  uint64_t a, x, y, ys, r, q, g;
  do
    a = random() % n;
  while (a == 0 || a == n - 2);
  y = random() % n;
  r = 1;
  q = 1;

  do {
    x = y;
    for (uint64_t i = 0; i < r; i++) {
      // y = y² + a mod n
      y = mult(y, y, n);
      y += a;
      if (y < a) {
        uint64_t maxim = UINT64_MAX;
        y += (maxim - n) + 1;
      }
      y %= n;
    }

    uint64_t k = 0;
    do {
      for (uint64_t i = 0; i < m && i < r - k; i++) {
        ys = y;

        // y = y² + a mod n
        y = mult(y, y, n);
        y += a;
        if (y < a) {
          uint64_t maxim = UINT64_MAX;
          y += (maxim - n) + 1;
        }
        y %= n;

        // q = q |x-y| mod n
        q = mult(q, (x > y) ? x - y : y - x, n);
      }
      g = std::gcd(q, n);
      k += m;
    } while (k < r && g == 1);

    r <<= 1;
  } while (g == 1);

  if (g == n) {
    do {
      // ys = ys² + a mod n
      ys = mult(ys, ys, n);
      ys += a;
      if (ys < a) {
        uint64_t maxim = UINT64_MAX;
        ys += (maxim - n) + 1;
      }
      ys %= n;

      g = std::gcd((x > ys) ? x - ys : ys - x, n);
    } while (g == 1);
  }

  return g;
}

int division_tentativa(int n) {
  /* for i in range(2, int(n**0.5) + 1): */
  for (int i = 2; i < pow(n, 0.5) + 1; i++) {
    if (n % i == 0)
      return i;
  }
  return n;
}

void update_map(uint64_t key, std::unordered_map<uint64_t, uint64_t> &map) {
  if (map.find(key) != map.end()) {
    map[key]++;
  } else {
    map[key] = 1;
  }
}

std::unordered_map<uint64_t, uint64_t> prime_factors(uint64_t n) {
  std::unordered_map<uint64_t, uint64_t> primes;
  /* std::vector<uint64_t> factors; */
  std::vector<uint64_t> factors;

  /* uint64_t factor = brent(n); */
  uint64_t factor = brent_pollard_factor(n);
  factors.push_back(n / factor);
  factors.push_back(factor);

  do {
    uint64_t m = factors[factors.size() - 1];
    factors.pop_back();

    if (m == 1)
      continue;

    if (MillerRabin(m)) {
      update_map(m, primes);

      // Remove the prime from the other factors
      for (int i = 0; i < factors.size(); i++) {
        uint64_t k = factors[i];
        if (k % m == 0) {
          do {
            k /= m;
            update_map(m, primes);
          } while (k % m == 0);

          factors[i] = k;
        }
      }
    } else {
      /* factor = (m < 100) ? division_tentativa(m) : brent(m); */
      factor = (m < 100) ? division_tentativa(m) : brent_pollard_factor(m);
      factors.push_back(m / factor);
      factors.push_back(factor);
    }
  } while (factors.size());

  return primes;
}

int main() {
  std::unordered_map<uint64_t, uint64_t> result = prime_factors(646899790);

  printf("{");
  for (auto i : result)
    printf("%lu:%lu ,", i.first, i.second);
  printf("}");

  return 0;
}