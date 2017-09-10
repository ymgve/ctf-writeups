__int64 __fastcall main(signed int argc, char **argv, char **a3)
{
  __int64 result; // rax@2
  char *buf2; // ST38_8@3
  unsigned int strlen0; // eax@3
  unsigned int strlen2; // eax@3
  unsigned int strlen1; // eax@3
  unsigned int v8; // eax@16
  __int64 v9; // rsi@22
  signed int i; // [sp+1Ch] [bp-174h]@3
  signed int j; // [sp+1Ch] [bp-174h]@6
  signed int k; // [sp+1Ch] [bp-174h]@9
  signed int l; // [sp+1Ch] [bp-174h]@16
  int num0; // [sp+20h] [bp-170h]@3
  int num1; // [sp+24h] [bp-16Ch]@3
  char *buf0; // [sp+28h] [bp-168h]@3
  char *buf1; // [sp+30h] [bp-160h]@3
  char hash0[32]; // [sp+40h] [bp-150h]@3
  char hash1[32]; // [sp+60h] [bp-130h]@3
  char hash2[32]; // [sp+80h] [bp-110h]@3
  char output[32]; // [sp+A0h] [bp-F0h]@16
  char hex0[48]; // [sp+C0h] [bp-D0h]@4
  char hex1[48]; // [sp+F0h] [bp-A0h]@7
  char hex2[48]; // [sp+120h] [bp-70h]@10
  char flag[56]; // [sp+150h] [bp-40h]@17
  __int64 canary; // [sp+188h] [bp-8h]@1

  canary = *MK_FP(__FS__, 40LL);
  if ( argc > 1 )
  {
    buf0 = (char *)malloc(4uLL);
    buf1 = (char *)malloc(4uLL);
    buf2 = (char *)malloc(4uLL);
    memset(buf0, 0, 4uLL);
    memset(buf1, 0, 4uLL);
    memset(buf2, 0, 4uLL);
    *(_DWORD *)buf0 = *(_DWORD *)argv[1];
    memcpy(buf2, argv[1] + 3, 6uLL);
    *(_DWORD *)buf1 = *((_DWORD *)argv[1] + 2);
    num0 = strtol(buf0, 0LL, 16);
    num1 = strtol(buf1, 0LL, 16);
    strlen0 = strlen(buf0);
    sha1(hash0, buf0, strlen0);
    strlen2 = strlen(buf2);
    sha1(hash2, buf2, strlen2);
    strlen1 = strlen(buf1);
    sha1(hash1, buf1, strlen1);
    for ( i = 0; i <= 19; ++i )
      sprintf(&hex0[2 * i], "%02x", (unsigned __int8)hash0[i]);
    for ( j = 0; j <= 19; ++j )
      sprintf(&hex1[2 * j], "%02x", (unsigned __int8)hash1[j]);
    for ( k = 0; k <= 19; ++k )
      sprintf(&hex2[2 * k], "%02x", (unsigned __int8)hash2[k]);
    if ( !strcmp(hex2, "69fc8b9b1cdfe47e6b51a6804fc1dbddba1ea1d9")
      && num0 < num1
      && !strncmp(hex0, buf0, 4uLL)
      && !strncmp(hex1, buf1, 4uLL) )
    {
      printf("gj, you got the flag: ");
      v8 = strlen(argv[1]);
      sha1(output, argv[1], v8);
      for ( l = 0; l <= 19; ++l )
        sprintf(&flag[2 * l], "%02x", (unsigned __int8)output[l]);
      printf("ASIS{%s}\n", flag);
      exit(0);
    }
    puts("Sorry, try harder :(");
    result = 0LL;
  }
  else
  {
    puts("give me flag... :D");
    result = 0LL;
  }
  v9 = *MK_FP(__FS__, 40LL) ^ canary;
  return result;
}