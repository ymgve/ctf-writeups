__int64 __fastcall main(signed int a1, char **a2, char **a3)
{
  char **v3; // r12@1
  vm_state *vm; // rbx@1
  void *v5; // rbp@2
  signed __int64 v6; // rsi@2
  void *v7; // r14@2
  char *v8; // rdx@2
  signed int v9; // er14@4
  void *gb_rom; // rbp@6
  _BYTE *v11; // r12@10
  __int64 v12; // rax@10
  void *v13; // rdi@11
  unsigned int v14; // er12@11
  unsigned int v15; // ebp@11
  _BYTE *v16; // rax@11
  __int16 v17; // cx@15
  _BYTE *memory_; // rdi@15
  __int16 v19; // ax@15
  _BYTE *memory__; // rdx@15
  int v21; // eax@16
  int somecounter; // eax@18
  void *dest; // rax@23
  void *src; // rdx@23
  int v25; // eax@24
  char v26; // al@26
  char v27; // al@27
  signed int v28; // ecx@27
  int v29; // eax@31
  char v30; // al@32
  int v31; // er13@41
  int numreturned; // eax@42
  _BYTE *v33; // rcx@44
  char v34; // dl@44
  char int_flags; // al@48
  char v36; // al@53
  char interrupts; // cl@54
  __int16 v38; // cx@59
  __int16 v39; // ax@59
  __int16 temp_pc; // ax@61
  _BYTE *opcode_addr; // r8@61
  unsigned __int64 primary_opcode; // rsi@61
  __int16 v43; // cx@62
  __int16 v44; // ax@62
  unsigned __int8 lcdc_y; // al@67
  char v47; // al@68
  _BYTE *v48; // rax@69
  char v49; // dl@69
  unsigned __int8 v50; // al@72
  unsigned __int8 v51; // al@72
  unsigned __int8 v52; // al@72
  char mem_FF40_LCDC; // cl@72
  unsigned __int8 mem_FF44_LY; // r10@72
  char *mem_bgmap; // r14@73
  __int64 v56; // r11@75
  char *mem_bgmap_indexer; // r8@76
  __int64 v58; // rdi@76
  _BYTE *memory___; // rax@76
  char v60; // si@76
  unsigned __int8 *v61; // rax@77
  char *v62; // rcx@78
  char *v63; // rsi@78
  int v64; // er15@79
  char v65; // dl@79
  _BYTE *v66; // rax@84
  _BYTE *v67; // rax@84
  char v68; // al@87
  __int16 v69; // cx@89
  __int16 v70; // ax@89
  __int16 v71; // cx@93
  __int16 v72; // ax@93
  __int64 v73; // rdi@112
  char v74; // si@112
  int v75; // eax@112
  char v76; // r8@113
  __int64 v77; // rdx@113
  signed __int64 v78; // r14@117
  signed __int64 v79; // r15@118
  __int64 v80; // rcx@119
  int v81; // edx@119
  unsigned __int8 v82; // cf@119
  __int16 v83; // r8@122
  __int16 v84; // di@122
  char v85; // cl@122
  unsigned __int16 v86; // di@122
  char v87; // si@122
  char v88; // r8@123
  int cycles_used; // ecx@126
  char v90; // cl@131
  __int16 v91; // cx@132
  unsigned __int16 v92; // si@133
  __int16 v93; // r8@133
  int v94; // edi@133
  char v95; // cl@133
  char v96; // cl@138
  __int64 v97; // rcx@140
  __int64 v98; // rcx@141
  char v99; // cl@142
  int v100; // eax@143
  unsigned __int16 v101; // si@146
  __int16 v102; // r8@146
  int v103; // edi@146
  char v104; // cl@146
  char v105; // cl@151
  __int64 v106; // rax@152
  __int64 v107; // rax@153
  unsigned __int8 v108; // r9@154
  int v109; // esi@154
  int v110; // edi@154
  char v111; // r8@154
  unsigned __int8 v112; // r9@154
  char v113; // cl@154
  int v114; // edi@154
  char v115; // r10@155
  char v116; // si@155
  __int64 regc; // rax@164
  int rega; // edx@164
  _BYTE *v119; // rdi@164
  unsigned __int8 v120; // si@164
  char rega_; // r8@164
  int v122; // ecx@164
  char v123; // al@164
  int v124; // ecx@164
  char v125; // r9@165
  char v126; // dl@165
  __int16 v127; // ax@174
  bool v128; // zf@174
  __int16 v129; // si@175
  __int16 v130; // cx@175
  __int16 v131; // ax@178
  __int16 v132; // cx@178
  __int16 v133; // di@179
  __int16 v134; // si@179
  char v135; // cl@179
  unsigned __int16 v136; // si@179
  char v137; // r8@179
  char v138; // r9@180
  char v139; // di@180
  __int16 v140; // ax@187
  __int16 v141; // si@188
  __int16 v142; // cx@188
  __int16 v143; // cx@190
  __int16 v144; // cx@198
  unsigned __int8 v145; // si@199
  unsigned __int8 v146; // r9@199
  __int16 v147; // cx@199
  unsigned __int8 v148; // si@199
  char v149; // r8@199
  __int16 v150; // cx@199
  unsigned __int16 v151; // di@199
  char v152; // r10@200
  char v153; // cl@200
  __int16 v154; // cx@209
  __int16 v155; // ax@209
  __int16 v156; // si@209
  __int16 v157; // ax@210
  bool v158; // sf@210
  __int16 v159; // si@211
  __int16 v160; // cx@211
  char v161; // r14@212
  char v162; // r15@212
  char *v163; // r10@213
  int v164; // er9@214
  int v165; // ecx@214
  char v166; // r11@214
  char v167; // dl@215
  signed int v168; // eax@215
  char v169; // r14@229
  char filtered_opcode; // cl@232
  char v171; // r9@233
  char v172; // al@238
  char *v173; // rcx@249
  signed int v174; // eax@249
  __int16 v175; // ax@251
  __int64 v176; // rcx@252
  signed int v177; // eax@252
  __int16 v178; // ax@253
  __int16 v179; // cx@255
  __int16 v180; // ax@255
  unsigned __int8 v181; // si@257
  unsigned __int8 v182; // si@259
  unsigned __int8 v183; // al@260
  unsigned __int8 v184; // al@264
  unsigned __int8 v185; // si@266
  char v186; // al@267
  __int16 v187; // di@269
  int v188; // eax@269
  int v189; // esi@269
  __int16 v190; // cx@269
  char v191; // al@269
  __int64 v192; // rax@274
  unsigned __int8 v193; // si@275
  char *v194; // rdi@276
  unsigned __int8 v195; // cl@277
  char v196; // r9@277
  __int16 v197; // ax@277
  unsigned __int8 v198; // cl@277
  char v199; // r8@277
  __int16 v200; // ax@277
  unsigned __int16 v201; // di@277
  char v202; // r10@278
  char v203; // al@278
  unsigned __int8 v204; // si@288
  char *v205; // rdi@289
  __int16 v206; // r9@290
  __int16 v207; // di@290
  char v208; // r8@290
  unsigned __int16 v209; // di@290
  char v210; // cl@290
  char v211; // r9@291
  signed int v212; // ecx@299
  char *v213; // rax@300
  char *v214; // rdi@302
  __int64 v215; // rax@306
  unsigned __int8 v216; // si@309
  unsigned __int8 v217; // cl@309
  char v218; // al@310
  unsigned __int8 v219; // si@311
  char v220; // al@312
  char v221; // al@313
  char v222; // al@314
  unsigned __int8 v223; // si@315
  unsigned __int8 v224; // al@316
  unsigned __int8 v225; // al@320
  char v226; // al@325
  unsigned int v227; // edx@327
  char v228; // si@330
  char v229; // r9@333
  char v230; // al@339
  char v231; // al@343
  __int16 v232; // cx@348
  __int16 v233; // di@352
  __int16 v234; // si@352
  char v235; // r8@352
  unsigned __int16 v236; // si@352
  char v237; // cl@352
  char v238; // r9@353
  char v239; // di@353
  __int16 v240; // cx@360
  __int16 v241; // ax@361
  __int16 v242; // si@362
  __int16 v243; // cx@362
  __int16 v244; // cx@367
  int v245; // esi@371
  unsigned int v246; // ecx@371
  __int16 v247; // ax@374
  char v248; // cl@376
  __int16 v249; // ax@377
  __int16 v250; // ax@380
  char v251; // cl@382
  char v252; // dl@384
  char v253; // cl@387
  char v254; // dl@391
  char v255; // si@393
  char v256; // r8@393
  __int16 v257; // ax@398
  char v258; // cl@400
  int v259; // esi@400
  int v260; // edi@400
  __int16 v261; // ax@402
  int v262; // ecx@403
  unsigned __int8 v263; // si@403
  int v264; // esi@403
  unsigned __int8 v265; // di@405
  char v266; // cl@407
  char v267; // si@407
  char v268; // dl@413
  signed int v269; // eax@413
  char *v270; // r8@415
  unsigned __int8 v271; // cl@415
  signed int v272; // edx@426
  char *v273; // rdi@427
  char v274; // cl@428
  char v275; // si@428
  char v276; // al@428
  char v277; // r8@428
  signed int v278; // edx@440
  char *v279; // rdi@441
  char v280; // cl@442
  char v281; // al@442
  char v282; // si@442
  char userinput; // [sp+27h] [bp-C1h]@64
  __int64 v284; // [sp+28h] [bp-C0h]@42
  __int64 v285; // [sp+30h] [bp-B8h]@42
  fd_set fdset; // [sp+38h] [bp-B0h]@42

  v3 = a2;
  vm = (vm_state *)calloc(1uLL, 0x68uLL);
  if ( !vm )
    goto EXIT;
  v5 = calloc(1uLL, 0x10002uLL);
  vm->memory = v5;
  v6 = 0x10000LL;
  v7 = calloc(1uLL, 0x5A00uLL);
  vm->video_memory = (__int64)v7;
  v8 = (char *)calloc(1uLL, 0x10000uLL);
  vm->window_memory = v8;
  if ( v7 == 0LL || v5 == 0LL || !v8 )
    goto EXIT;
  v9 = -1;
  vm->dma_destination = (char *)v5 + 0xFE00;
  if ( a1 > 1 )
  {
    v6 = 0LL;
    v9 = strtol(v3[1], 0LL, 0);
  }
  printf("\x1B[2J", v6, v8);
  gb_rom = calloc(1uLL, 0x8000uLL);
  if ( !gb_rom )
EXIT:
    exit(1);
  if ( fread(gb_rom, 1uLL, 0x8000uLL, stdin) != 0x8000
    || (memcpy(vm->memory, gb_rom, 0x8000uLL),
        v11 = vm->memory,
        LODWORD(v12) = modify_title_to_cstring(vm->memory + 256),
        vm->name_string = v12,
        fprintf(stderr, "Title: %s\n", v12),
        *((_WORD *)v11 + 164)) )
  {
    free(gb_rom);
    goto EXIT;
  }
  v13 = gb_rom;
  v14 = 0;
  v15 = 0;
  free(v13);
  printf("\x1B[?25l");
  fflush(stdout);
  setvbuf(stdout, 0LL, 0, 0x6400uLL);
  v16 = vm->memory;
  *(_WORD *)&vm->reg_flags = 0x1B0;
  *(_WORD *)&vm->reg_C = 0x13;
  *(_WORD *)&vm->reg_E = 0xD8;
  *(_WORD *)&vm->reg_L = 0x14D;
  vm->reg_SP = 0xFFFEu;
  vm->reg_PC = 0x100;
  v16[0xFF05] = 0;
  vm->memory[0xFF06] = 0;
  vm->memory[0xFF07] = 0;
  vm->memory[0xFF10] = 0x80u;
  vm->memory[0xFF11] = 0xBFu;
  vm->memory[0xFF12] = 0xF3u;
  vm->memory[0xFF14] = 0xBFu;
  vm->memory[0xFF16] = 0x3F;
  vm->memory[0xFF17] = 0;
  vm->memory[0xFF19] = -65;
  vm->memory[0xFF1A] = 127;
  vm->memory[0xFF1B] = -1;
  vm->memory[0xFF1C] = -97;
  vm->memory[65309] = -65;
  vm->memory[65312] = -1;
  vm->memory[65313] = 0;
  vm->memory[65314] = 0;
  vm->memory[65315] = -65;
  vm->memory[65316] = 119;
  vm->memory[65317] = -13;
  vm->memory[65318] = -15;
  vm->memory[0xFF40] = 0x90u;
  vm->memory[0xFF42] = 0;
  vm->memory[0xFF43] = 0;
  vm->memory[0xFF45] = 0;
  vm->memory[0xFF47] = -4;
  vm->memory[0xFF48] = -1;
  vm->memory[0xFF49] = -1;
  vm->memory[0xFF4A] = 0;
  vm->memory[0xFF4B] = 0;
  vm->memory[0xFFFF] = 0;
  vm->memory[65350] = -1;
  vm->field_50 = 0;
  vm->somecounter = 0;
  vm->field_5C = 0;
  vm->field_60 = 0;
  vm->cycles_used = 0;
  vm->joy_input = 0;
  vm->field_44 = 0;
  LODWORD(vm->field_48) = 0x41000000;
  vm->do_output = 0;
  while ( 1 )
  {
    if ( v9 == -1 )
    {
      v31 = -1;
    }
    else
    {
      v31 = v9 - 1;
      if ( !v9 )
        break;
    }
    memset(&fdset, 0, sizeof(fdset));
    fdset.fds_bits[0] |= 1uLL;
    v284 = 0LL;
    v285 = 0LL;
    numreturned = select(1, &fdset, 0LL, 0LL, (struct timeval *)&v284);
    if ( numreturned == -1 )
      break;
    if ( numreturned )
    {
      if ( read(0, &userinput, 1uLL) != 1 )
        break;
      switch ( userinput )
      {
        default:
          break;
        case 'q':
          goto GOODEXIT;
        case 'w':
          vm->joy_input |= 4u;
          break;
        case 'u':
          vm->joy_input |= 0x40u;
          break;
        case 's':
          vm->joy_input |= 8u;
          break;
        case 'j':
          vm->joy_input |= 0x10u;
          break;
        case 'i':
          vm->joy_input |= 0x80u;
          break;
        case 'k':
          vm->joy_input |= 0x20u;
          break;
        case 'd':
          vm->joy_input |= 1u;
          break;
        case 'a':
          vm->joy_input |= 2u;
          break;
      }
    }
    vm->memory[0xFF00] |= 0xFu;
    v33 = vm->memory;
    v34 = vm->memory[0xFF00];
    if ( !(v34 & 0x10) )
    {
      v33[0xFF00] = v34 & ~(vm->joy_input & 0xF);
      v33 = vm->memory;
      v34 = vm->memory[0xFF00];
    }
    if ( !(v34 & 0x20) )
      v33[0xFF00] = v34 & ~((unsigned __int8)vm->joy_input >> 4);
    int_flags = vm->int_flags;
    if ( int_flags < 0 )
    {
      v36 = int_flags & 0x7F;
      vm->int_flags = v36;
    }
    else
    {
      if ( int_flags & 0x40 )
      {
        int_flags &= 0xFEu;
        vm->int_flags = int_flags;
      }
      if ( int_flags & 0x20 )
        int_flags |= 1u;
      v36 = int_flags & 0x9F;
      vm->int_flags = v36;
    }
    memory_ = vm->memory;
    memory__ = vm->memory;
    interrupts = vm->memory[0xFFFF] & vm->memory[0xFF0F];
    if ( !interrupts )
    {
      if ( v36 & 1 )
      {
LABEL_56:
        if ( interrupts & 4 )
        {
          memory_[0xFF0F] &= 0xFBu;
          vm->int_flags = 0;
          v71 = vm->reg_PC;
          memory_ = vm->memory;
          v72 = vm->reg_SP - 2;
          memory__ = memory_;
          vm->reg_SP = v72;
          *(_WORD *)&memory_[(unsigned __int16)v72] = v71;
          vm->reg_PC = 80;
        }
        else if ( interrupts & 8 )
        {
          memory_[0xFF0F] &= 0xF7u;
          vm->int_flags = 0;
          v69 = vm->reg_PC;
          memory_ = vm->memory;
          v70 = vm->reg_SP - 2;
          memory__ = memory_;
          vm->reg_SP = v70;
          *(_WORD *)&memory_[(unsigned __int16)v70] = v69;
          vm->reg_PC = 88;
        }
        else if ( interrupts & 0x10 )
        {
          memory_[0xFF0F] &= 0xEFu;
          vm->int_flags = 0;
          v38 = vm->reg_PC;
          memory_ = vm->memory;
          v39 = vm->reg_SP - 2;
          memory__ = memory_;
          vm->reg_SP = v39;
          *(_WORD *)&memory_[(unsigned __int16)v39] = v38;
          v21 = vm->cycles_used;
          vm->reg_PC = 96;
          if ( (unsigned int)v21 > 1 )
            goto LABEL_17;
LABEL_60:
          if ( vm->field_44 )
            goto LABEL_18;
          goto LABEL_61;
        }
      }
LABEL_16:
      v21 = vm->cycles_used;
      if ( (unsigned int)v21 > 1 )
        goto LABEL_17;
      goto LABEL_60;
    }
    vm->field_44 = 0;
    if ( v36 & 1 )
    {
      if ( interrupts & 1 )
      {
        memory_[0xFF0F] &= 0xFEu;
        vm->int_flags = 0;
        v43 = vm->reg_PC;
        memory_ = vm->memory;
        v44 = vm->reg_SP - 2;
        memory__ = memory_;
        vm->reg_SP = v44;
        *(_WORD *)&memory_[(unsigned __int16)v44] = v43;
        vm->reg_PC = 0x40;
      }
      else
      {
        if ( !(interrupts & 2) )
          goto LABEL_56;
        memory_[65295] &= 0xFDu;
        vm->int_flags = 0;
        v17 = vm->reg_PC;
        memory_ = vm->memory;
        v19 = vm->reg_SP - 2;
        memory__ = memory_;
        vm->reg_SP = v19;
        *(_WORD *)&memory_[(unsigned __int16)v19] = v17;
        vm->reg_PC = 0x48;
      }
      goto LABEL_16;
    }
    v21 = vm->cycles_used;
    if ( (unsigned int)v21 > 1 )
    {
LABEL_17:
      vm->cycles_used = v21 - 1;
      goto LABEL_18;
    }
LABEL_61:
    temp_pc = vm->reg_PC;
    opcode_addr = &memory_[vm->reg_PC];
    primary_opcode = *opcode_addr;
    switch ( (_BYTE)primary_opcode )
    {
      case 0xFE:
        v83 = opcode_addr[1];
        v84 = vm->reg_A;
        vm->reg_flags = 0x40;
        v85 = v84;
        v86 = v84 - v83;
        v87 = v83;
        if ( v86 )
        {
          v88 = 96;
          if ( v86 > 0xFFu )
          {
            vm->reg_flags = 80;
            v88 = 112;
          }
        }
        else
        {
          vm->reg_flags = -64;
          v88 = -32;
        }
        if ( ((v85 & 0xF) - (v87 & 0xF)) & 0x10 )
          vm->reg_flags = v88;
        cycles_used = 2;
        vm->reg_PC = temp_pc + 2;
        goto INSTR_DONE;
      case 0xFB:
        vm->int_flags |= 0xA0u;
        cycles_used = 1;
        vm->reg_PC = temp_pc + 1;
        goto INSTR_DONE;
      case 0xFA:
        v90 = memory_[*(_WORD *)(opcode_addr + 1)];
        vm->reg_PC = temp_pc + 3;
        vm->reg_A = v90;
        cycles_used = 4;
        goto INSTR_DONE;
      case 0xF9:
        v91 = *(_WORD *)&vm->reg_L;
        vm->reg_PC = temp_pc + 1;
        vm->reg_SP = v91;
        cycles_used = 2;
        goto INSTR_DONE;
      case 0xF8:
        v92 = opcode_addr[1];
        v93 = vm->reg_SP;
        v94 = v92 + vm->reg_SP;
        v95 = vm->reg_flags & 0x8F;
        vm->reg_flags = v95;
        if ( v94 > 0xFFFF )
        {
          v95 |= 0x10u;
          vm->reg_flags = v95;
        }
        *(_WORD *)&vm->reg_L = v94;
        if ( ((v93 & 0xFFF) + (v92 & 0xFFF)) & 0x1000 )
          v95 |= 0x20u;
        vm->reg_PC = temp_pc + 2;
        vm->reg_flags = v95 & 0x7F;
        cycles_used = 3;
        goto INSTR_DONE;
      case 0xF6:
        v96 = vm->reg_A | opcode_addr[1];
        vm->reg_A = v96;
        vm->reg_PC = temp_pc + 2;
        vm->reg_flags = (unsigned __int8)v96 < 1u ? 0x80 : 0;
        cycles_used = 2;
        goto INSTR_DONE;
      case 0xF3:
        vm->int_flags |= 0xC0u;
        cycles_used = 1;
        vm->reg_PC = temp_pc + 1;
        goto INSTR_DONE;
      case 0xF2:
        v97 = vm->reg_C;
        BYTE1(v97) = 0xFFu;
        LOBYTE(v97) = memory_[v97];
        vm->reg_PC = temp_pc + 1;
        vm->reg_A = v97;
        cycles_used = 2;
        goto INSTR_DONE;
      case 0xF0:
        v98 = opcode_addr[1];
        BYTE1(v98) = -1;
        LOBYTE(v98) = memory_[v98];
        vm->reg_PC = temp_pc + 2;
        vm->reg_A = v98;
        cycles_used = 3;
        goto INSTR_DONE;
      case 0xEE:
        v99 = vm->reg_A ^ opcode_addr[1];
        vm->reg_A = v99;
        vm->reg_PC = temp_pc + 2;
        vm->reg_flags = (unsigned __int8)v99 < 1u ? 0x80 : 0;
        cycles_used = 2;
        goto INSTR_DONE;
      case 0xED:
        v100 = vm->reg_C;
        cycles_used = 2;
        BYTE1(v100) = 0xFFu;
        memory_[v100] ^= vm->reg_A;
        ++vm->reg_PC;
        memory__ = vm->memory;
        goto INSTR_DONE;
      case 0xEA:
        cycles_used = 4;
        memory_[*(_WORD *)(opcode_addr + 1)] = vm->reg_A;
        vm->reg_PC += 3;
        memory__ = vm->memory;
        goto INSTR_DONE;
      case 0xE9:
        cycles_used = 1;
        vm->reg_PC = *(_WORD *)&vm->reg_L;
        goto INSTR_DONE;
      case 0xE8:
        v101 = opcode_addr[1];
        v102 = vm->reg_SP;
        v103 = v101 + vm->reg_SP;
        v104 = vm->reg_flags & 0x8F;
        vm->reg_flags = v104;
        if ( v103 > 0xFFFF )
        {
          v104 |= 0x10u;
          vm->reg_flags = v104;
        }
        vm->reg_SP = v103;
        if ( ((v102 & 0xFFF) + (v101 & 0xFFF)) & 0x1000 )
          v104 |= 0x20u;
        vm->reg_PC = temp_pc + 2;
        vm->reg_flags = v104 & 0x7F;
        cycles_used = 4;
        goto INSTR_DONE;
      case 0xE6:
        v105 = vm->reg_A & opcode_addr[1];
        vm->reg_A = v105;
        vm->reg_PC = temp_pc + 2;
        vm->reg_flags = (unsigned __int8)v105 < 1u ? -96 : 32;
        cycles_used = 2;
        goto INSTR_DONE;
      case 0xE2:
        v106 = vm->reg_C;
        cycles_used = 2;
        BYTE1(v106) = -1;
        memory_[v106] = vm->reg_A;
        ++vm->reg_PC;
        memory__ = vm->memory;
        goto INSTR_DONE;
      case 0xE0:
        v107 = opcode_addr[1];
        cycles_used = 3;
        BYTE1(v107) = -1;
        memory_[v107] = vm->reg_A;
        vm->reg_PC += 2;
        memory__ = vm->memory;
        goto INSTR_DONE;
      case 0xDE:
        v108 = vm->reg_flags;
        v109 = opcode_addr[1];
        v110 = vm->reg_A;
        vm->reg_flags = 64;
        v111 = v109;
        v112 = (v108 >> 4) & 1;
        v113 = v110;
        v114 = v110 - v109 - v112;
        if ( (_BYTE)v114 )
        {
          v115 = 80;
          v116 = 64;
        }
        else
        {
          vm->reg_flags = -64;
          v115 = -48;
          v116 = -64;
        }
        if ( (unsigned __int16)v114 > 0xFFu )
        {
          vm->reg_flags = v115;
          v116 = v115;
        }
        if ( ((v113 & 0xF) - (v111 & 0xF)) & 0x10 )
        {
          v116 |= 0x20u;
          vm->reg_flags = v116;
        }
        if ( (((v113 - v111) & 0xF) - v112) & 0x10 )
          vm->reg_flags = v116 | 0x20;
        vm->reg_A = v114;
        cycles_used = 2;
        vm->reg_PC = temp_pc + 2;
        goto INSTR_DONE;
      case 0xDD:
        regc = vm->reg_C;
        rega = vm->reg_A;
        BYTE1(regc) = 0xFFu;
        v119 = &memory_[regc];
        v120 = ((unsigned __int8)vm->reg_flags >> 4) & 1;
        rega_ = vm->reg_A;
        v122 = *v119;
        vm->reg_flags = 64;
        v123 = v122;
        v124 = v122 - rega - v120;
        if ( (_BYTE)v124 )
        {
          v125 = 0x50;
          v126 = 0x40;
        }
        else
        {
          vm->reg_flags = 0xC0u;
          v125 = 0xD0u;
          v126 = 0xC0u;
        }
        if ( (unsigned __int16)v124 > 0xFFu )
        {
          vm->reg_flags = v125;
          v126 = v125;
        }
        if ( ((v123 & 0xF) - (rega_ & 0xF)) & 0x10 )
        {
          v126 |= 0x20u;
          vm->reg_flags = v126;
        }
        if ( (((v123 - rega_) & 0xF) - v120) & 0x10 )
          vm->reg_flags = v126 | 0x20;
        *v119 = v124;
        cycles_used = 4;
        ++vm->reg_PC;
        memory__ = vm->memory;
        goto INSTR_DONE;
      case 0xDC:
        v127 = temp_pc + 3;
        v128 = (vm->reg_flags & 0x10) == 0;
        cycles_used = 3;
        vm->reg_PC = v127;
        if ( !v128 )
        {
          v129 = *(_WORD *)(opcode_addr + 1);
          v130 = vm->reg_SP - 2;
          vm->reg_SP = v130;
          *(_WORD *)&memory_[(unsigned __int16)v130] = v127;
          vm->reg_PC = v129;
          cycles_used = 6;
        }
        goto INSTR_DONE;
      case 0xDA:
        if ( vm->reg_flags & 0x10 )
        {
          cycles_used = 4;
          vm->reg_PC = *(_WORD *)(opcode_addr + 1);
        }
        else
        {
          cycles_used = 3;
          vm->reg_PC = temp_pc + 3;
        }
        goto INSTR_DONE;
      case 0xD9:
        v131 = vm->reg_SP;
        v132 = *(_WORD *)&memory_[vm->reg_SP];
        vm->int_flags = 1;
        vm->reg_SP = v131 + 2;
        vm->reg_PC = v132;
        cycles_used = 4;
        goto INSTR_DONE;
      case 0xD6:
        v133 = opcode_addr[1];
        v134 = vm->reg_A;
        vm->reg_flags = 64;
        v135 = v134;
        v136 = v134 - v133;
        v137 = v133;
        if ( v136 )
        {
          v138 = 80;
          v139 = 64;
        }
        else
        {
          vm->reg_flags = -64;
          v138 = -48;
          v139 = -64;
        }
        if ( v136 > 0xFFu )
        {
          vm->reg_flags = v138;
          v139 = v138;
        }
        if ( ((v135 & 0xF) - (v137 & 0xF)) & 0x10 )
          vm->reg_flags = v139 | 0x20;
        vm->reg_A = v136;
        cycles_used = 2;
        vm->reg_PC = temp_pc + 2;
        goto INSTR_DONE;
      case 0xD4:
        v140 = temp_pc + 3;
        v128 = (vm->reg_flags & 0x10) == 0;
        cycles_used = 3;
        vm->reg_PC = v140;
        if ( v128 )
        {
          v141 = *(_WORD *)(opcode_addr + 1);
          v142 = vm->reg_SP - 2;
          vm->reg_SP = v142;
          *(_WORD *)&memory_[(unsigned __int16)v142] = v140;
          vm->reg_PC = v141;
          cycles_used = 6;
        }
        goto INSTR_DONE;
      case 0xD8:
        if ( vm->reg_flags & 0x10 )
        {
          v143 = *(_WORD *)&memory_[vm->reg_SP];
          vm->reg_SP += 2;
          vm->reg_PC = v143;
          cycles_used = 4;
        }
        else
        {
          cycles_used = 2;
          vm->reg_PC = temp_pc + 1;
        }
        goto INSTR_DONE;
      case 0xD2:
        if ( vm->reg_flags & 0x10 )
        {
          cycles_used = 3;
          vm->reg_PC = temp_pc + 3;
        }
        else
        {
          cycles_used = 4;
          vm->reg_PC = *(_WORD *)(opcode_addr + 1);
        }
        goto INSTR_DONE;
      case 0xD0:
        if ( vm->reg_flags & 0x10 )
        {
          cycles_used = 2;
          vm->reg_PC = temp_pc + 1;
        }
        else
        {
          v144 = *(_WORD *)&memory_[vm->reg_SP];
          vm->reg_SP += 2;
          vm->reg_PC = v144;
          cycles_used = 4;
        }
        goto INSTR_DONE;
      case 0xCE:
        v145 = vm->reg_flags;
        v146 = opcode_addr[1];
        v147 = vm->reg_A;
        vm->reg_flags = 0;
        v148 = (v145 >> 4) & 1;
        v149 = v147;
        v150 = v148 + v147;
        v151 = v150 + v146;
        if ( (_BYTE)v150 + v146 )
        {
          v152 = 16;
          v153 = 0;
        }
        else
        {
          vm->reg_flags = -128;
          v152 = -112;
          v153 = -128;
        }
        if ( v151 > 0xFFu )
        {
          vm->reg_flags = v152;
          v153 = v152;
        }
        if ( ((v149 & 0xF) + (v146 & 0xF)) & 0x10 )
        {
          v153 |= 0x20u;
          vm->reg_flags = v153;
        }
        if ( (((v146 + v149) & 0xF) + v148) & 0x10 )
          vm->reg_flags = v153 | 0x20;
        vm->reg_A = v151;
        cycles_used = 2;
        vm->reg_PC = temp_pc + 2;
        goto INSTR_DONE;
      case 0xCD:
        v154 = vm->reg_SP;
        v155 = temp_pc + 3;
        vm->reg_PC = v155;
        v156 = *(_WORD *)(opcode_addr + 1);
        v154 -= 2;
        vm->reg_SP = v154;
        *(_WORD *)&memory_[(unsigned __int16)v154] = v155;
        vm->reg_PC = v156;
        cycles_used = 6;
        goto INSTR_DONE;
      case 0xCC:
        v157 = temp_pc + 3;
        v158 = vm->reg_flags < 0;
        cycles_used = 3;
        vm->reg_PC = v157;
        if ( v158 )
        {
          v159 = *(_WORD *)(opcode_addr + 1);
          v160 = vm->reg_SP - 2;
          vm->reg_SP = v160;
          *(_WORD *)&memory_[(unsigned __int16)v160] = v157;
          vm->reg_PC = v159;
          cycles_used = 6;
        }
        goto INSTR_DONE;
      case 0xCB:
        v161 = opcode_addr[1];
        v162 = opcode_addr[1] & 7;
        if ( v162 == 6 )
          v163 = &memory_[*(_WORD *)&vm->reg_L];
        else
          v163 = (char *)&vm->memory + register_byte_offsets[(unsigned __int64)(opcode_addr[1] & 7)];
        v164 = (unsigned __int8)*v163;
        v165 = (v161 & 0x38) >> 3;
        v166 = v161 & 0xF8;
        if ( !(v161 & 0xF8) )
        {
          v167 = __ROL1__(v164, 1);
          *v163 = v167;
          v168 = (unsigned __int8)v167 < 1u ? -112 : 16;
          if ( !v167 )
            v166 = -128;
          vm->reg_flags = v166;
          if ( (char)v164 >= 0 )
            goto LABEL_221;
LABEL_218:
          vm->reg_flags = v168;
          temp_pc = vm->reg_PC;
          memory__ = vm->memory;
          goto LABEL_219;
        }
        if ( v166 == 8 )
        {
          v231 = ((unsigned __int8)v164 >> 1) | ((v164 & 1) << 7);
          *v163 = v231;
          vm->reg_flags = (unsigned __int8)v231 < 1u ? 0x80 : 0;
          if ( v164 & 1 )
          {
            vm->reg_flags = (unsigned __int8)v231 < 1u ? -112 : 16;
            temp_pc = vm->reg_PC;
            memory__ = vm->memory;
            goto LABEL_219;
          }
          goto LABEL_221;
        }
        if ( v166 == 16 )
        {
          v230 = 2 * v164 | ((unsigned __int8)vm->reg_flags >> 4) & 1;
          *v163 = v230;
          if ( !v230 )
            v166 = -112;
          vm->reg_flags = (unsigned __int8)v230 < 1u ? 0x80 : 0;
          if ( (char)v164 < 0 )
          {
            vm->reg_flags = v166;
            temp_pc = vm->reg_PC;
            memory__ = vm->memory;
            goto LABEL_219;
          }
          goto LABEL_221;
        }
        if ( v166 == 24 )
        {
          v227 = ((unsigned __int8)*v163 >> 1) | ((vm->reg_flags & 0x10u) >= 1 ? 0xFFFFFF80 : 0);
          goto LABEL_328;
        }
        if ( v166 == 32 )
        {
          *v163 = 2 * v164;
          v168 = (unsigned __int8)(2 * v164) < 1u ? -112 : 16;
          vm->reg_flags = (unsigned __int8)(2 * v164) < 1u ? 0x80 : 0;
          if ( (char)v164 < 0 )
            goto LABEL_218;
          goto LABEL_221;
        }
        if ( v166 == 40 )
        {
          v227 = ((unsigned __int8)*v163 >> 1) | v164 & 0xFFFFFF80;
          goto LABEL_328;
        }
        if ( v166 == 48 )
        {
          v229 = __ROL1__(v164, 4);
          *v163 = v229;
          memory__ = vm->memory;
          vm->reg_flags = (unsigned __int8)v229 < 1u ? 0x80 : 0;
          temp_pc = vm->reg_PC;
          goto LABEL_219;
        }
        if ( v166 == 56 )
        {
          LOBYTE(v227) = (unsigned __int8)v164 >> 1;
LABEL_328:
          *v163 = v227;
          v168 = (unsigned __int8)v227 < 1u ? -112 : 16;
          vm->reg_flags = (unsigned __int8)v227 < 1u ? 0x80 : 0;
          if ( v164 & 1 )
            goto LABEL_218;
LABEL_221:
          temp_pc = vm->reg_PC;
          memory__ = vm->memory;
LABEL_219:
          vm->reg_PC = temp_pc + 2;
          cycles_used = 2 * (v162 == 6) + 2;
          goto INSTR_DONE;
        }
        v169 = v161 & 0xC0;
        if ( v169 == 64 )
        {
          v228 = vm->reg_flags & 0x3F;
          v82 = _bittest(&v164, v165);
          vm->reg_flags = v228 | 0x20;
          if ( !v82 )
            vm->reg_flags = v228 | 0xA0;
          goto LABEL_219;
        }
        if ( v169 == -128 )
        {
          *v163 = ~(1 << v165) & v164;
          temp_pc = vm->reg_PC;
          memory__ = vm->memory;
          goto LABEL_219;
        }
        if ( v169 == -64 )
        {
          *v163 = (1 << v165) | v164;
          goto LABEL_221;
        }
LABEL_232:
        filtered_opcode = primary_opcode & 0xC7;
COMPARE_REST:
        v171 = primary_opcode & 0xCF;
        if ( (primary_opcode & 0xCF) == 1 )
        {
          *(_WORD *)((char *)&vm->memory + register_word_offsets[(primary_opcode >> 4) & 3]) = *(_WORD *)(opcode_addr + 1);
          cycles_used = 3;
          vm->reg_PC += 3;
        }
        else
        {
          switch ( v171 )
          {
            case 3:
              v192 = register_word_offsets[(primary_opcode >> 4) & 3];
              cycles_used = 2;
              ++*(_WORD *)((char *)&vm->memory + v192);
              ++vm->reg_PC;
              break;
            case 9:
              v187 = *(_WORD *)&vm->reg_L;
              v188 = *(_WORD *)((char *)&vm->memory + register_word_offsets[(primary_opcode >> 4) & 3]);
              v189 = v188 + *(_WORD *)&vm->reg_L;
              v190 = v188;
              v191 = vm->reg_flags & 0x8F;
              vm->reg_flags = v191;
              if ( v189 > 0xFFFF )
              {
                v191 |= 0x10u;
                vm->reg_flags = v191;
              }
              if ( ((unsigned __int16)((v187 & 0xFFF) + (v190 & 0xFFF)) >> 8) & 0x10 )
                vm->reg_flags = v191 | 0x20;
              *(_WORD *)&vm->reg_L = v189;
              ++vm->reg_PC;
              cycles_used = 2;
              break;
            case 11:
              v215 = register_word_offsets[(primary_opcode >> 4) & 3];
              cycles_used = 2;
              --*(_WORD *)((char *)&vm->memory + v215);
              ++vm->reg_PC;
              break;
            default:
              if ( (primary_opcode & 0xC0) == 0x40 )
              {
                v212 = (signed int)(primary_opcode & 0x38) >> 3;
                if ( (primary_opcode & 7) == 6 )
                  v213 = &memory_[*(_WORD *)&vm->reg_L];
                else
                  v213 = (char *)&vm->memory + register_byte_offsets[primary_opcode & 7];
                if ( v212 == 6 )
                  v214 = &memory_[*(_WORD *)&vm->reg_L];
                else
                  v214 = (char *)&vm->memory + register_byte_offsets[v212];
                *v214 = *v213;
                ++vm->reg_PC;
                memory__ = vm->memory;
                if ( v212 == 6 || (cycles_used = 1, (primary_opcode & 7) == 6) )
                  cycles_used = 2;
              }
              else
              {
                v172 = primary_opcode & 0xF8;
                if ( (primary_opcode & 0xF8) == 0x80u )
                {
                  v204 = primary_opcode & 7;
                  if ( v204 == 6 )
                    v205 = &memory_[*(_WORD *)&vm->reg_L];
                  else
                    v205 = (char *)&vm->memory + register_byte_offsets[(unsigned __int64)v204];
                  v206 = (unsigned __int8)*v205;
                  v207 = vm->reg_A;
                  vm->reg_flags = 0;
                  v208 = v207;
                  v209 = v206 + v207;
                  v210 = v206;
                  if ( (_BYTE)v209 )
                  {
                    v211 = 16;
                    v172 = 0;
                  }
                  else
                  {
                    vm->reg_flags = -128;
                    v211 = -112;
                  }
                  if ( v209 > 0xFFu )
                  {
                    vm->reg_flags = v211;
                    v172 = v211;
                  }
                  if ( ((v208 & 0xF) + (v210 & 0xF)) & 0x10 )
                    vm->reg_flags = v172 | 0x20;
                  ++vm->reg_PC;
                  vm->reg_A = v209;
                  cycles_used = (v204 == 6) + 1;
                }
                else
                {
                  switch ( v172 )
                  {
                    case 0x88:
                      v193 = primary_opcode & 7;
                      if ( v193 == 6 )
                        v194 = &memory_[*(_WORD *)&vm->reg_L];
                      else
                        v194 = (char *)&vm->memory + register_byte_offsets[(unsigned __int64)v193];
                      v195 = vm->reg_flags;
                      v196 = *v194;
                      v197 = vm->reg_A;
                      vm->reg_flags = 0;
                      v198 = (v195 >> 4) & 1;
                      v199 = v197;
                      v200 = v198 + v197;
                      v201 = v200 + (unsigned __int8)v196;
                      if ( (_BYTE)v200 + v196 )
                      {
                        v202 = 16;
                        v203 = 0;
                      }
                      else
                      {
                        vm->reg_flags = -128;
                        v202 = -112;
                        v203 = -128;
                      }
                      if ( v201 > 0xFFu )
                      {
                        vm->reg_flags = v202;
                        v203 = v202;
                      }
                      if ( ((v199 & 0xF) + (v196 & 0xF)) & 0x10 )
                      {
                        v203 |= 0x20u;
                        vm->reg_flags = v203;
                      }
                      if ( (((v196 + v199) & 0xF) + v198) & 0x10 )
                        vm->reg_flags = v203 | 0x20;
                      ++vm->reg_PC;
                      vm->reg_A = v201;
                      cycles_used = (v193 == 6) + 1;
                      break;
                    case 0x90:
                      v219 = primary_opcode & 7;
                      if ( v219 == 6 )
                      {
                        v222 = do_compare(vm, vm->reg_A, memory_[*(_WORD *)&vm->reg_L], 0);
                        ++vm->reg_PC;
                        vm->reg_A = v222;
                        cycles_used = 2;
                        memory__ = vm->memory;
                      }
                      else
                      {
                        v220 = do_compare(
                                 vm,
                                 vm->reg_A,
                                 *((_BYTE *)&vm->memory + register_byte_offsets[(unsigned __int64)v219]),
                                 0);
                        ++vm->reg_PC;
                        vm->reg_A = v220;
                        cycles_used = 1;
                        memory__ = vm->memory;
                      }
                      break;
                    case 0x98:
                      v216 = primary_opcode & 7;
                      v217 = ((unsigned __int8)vm->reg_flags >> 4) & 1;
                      if ( v216 == 6 )
                      {
                        v221 = do_compare(vm, vm->reg_A, memory_[*(_WORD *)&vm->reg_L], v217);
                        ++vm->reg_PC;
                        vm->reg_A = v221;
                        cycles_used = 2;
                        memory__ = vm->memory;
                      }
                      else
                      {
                        v218 = do_compare(
                                 vm,
                                 vm->reg_A,
                                 *((_BYTE *)&vm->memory + register_byte_offsets[(unsigned __int64)v216]),
                                 v217);
                        ++vm->reg_PC;
                        vm->reg_A = v218;
                        cycles_used = 1;
                        memory__ = vm->memory;
                      }
                      break;
                    case 0xA0:
                      v223 = primary_opcode & 7;
                      if ( v223 == 6 )
                      {
                        v225 = memory_[*(_WORD *)&vm->reg_L];
                        v128 = (v225 & vm->reg_A) == 0;
                        vm->reg_A &= v225;
                        if ( v128 )
                        {
                          vm->reg_flags = -96;
                          ++vm->reg_PC;
                          cycles_used = 2;
                        }
                        else
                        {
                          vm->reg_flags = 32;
                          ++vm->reg_PC;
                          cycles_used = 2;
                        }
                      }
                      else
                      {
                        v224 = *((_BYTE *)&vm->memory + register_byte_offsets[(unsigned __int64)v223]);
                        v128 = (v224 & vm->reg_A) == 0;
                        vm->reg_A &= v224;
                        if ( v128 )
                        {
                          vm->reg_flags = -96;
                          ++vm->reg_PC;
                          cycles_used = 1;
                        }
                        else
                        {
                          vm->reg_flags = 32;
                          ++vm->reg_PC;
                          cycles_used = 1;
                        }
                      }
                      break;
                    case 0xA8:
                      v185 = primary_opcode & 7;
                      if ( v185 == 6 )
                      {
                        v226 = memory_[*(_WORD *)&vm->reg_L];
                        v128 = v226 == vm->reg_A;
                        vm->reg_A ^= v226;
                        if ( v128 )
                        {
                          vm->reg_flags = -128;
                          ++vm->reg_PC;
                          cycles_used = 2;
                        }
                        else
                        {
                          vm->reg_flags = 0;
                          ++vm->reg_PC;
                          cycles_used = 2;
                        }
                      }
                      else
                      {
                        v186 = *((_BYTE *)&vm->memory + register_byte_offsets[(unsigned __int64)v185]);
                        v128 = v186 == vm->reg_A;
                        vm->reg_A ^= v186;
                        if ( v128 )
                        {
                          vm->reg_flags = -128;
                          ++vm->reg_PC;
                          cycles_used = 1;
                        }
                        else
                        {
                          vm->reg_flags = 0;
                          ++vm->reg_PC;
                          cycles_used = 1;
                        }
                      }
                      break;
                    case 0xB0:
                      v182 = primary_opcode & 7;
                      if ( v182 == 6 )
                      {
                        v184 = memory_[*(_WORD *)&vm->reg_L];
                        v128 = (v184 | vm->reg_A) == 0;
                        vm->reg_A |= v184;
                        if ( v128 )
                        {
                          vm->reg_flags = -128;
                          ++vm->reg_PC;
                          cycles_used = 2;
                        }
                        else
                        {
                          vm->reg_flags = 0;
                          ++vm->reg_PC;
                          cycles_used = 2;
                        }
                      }
                      else
                      {
                        v183 = *((_BYTE *)&vm->memory + register_byte_offsets[(unsigned __int64)v182]);
                        v128 = (v183 | vm->reg_A) == 0;
                        vm->reg_A |= v183;
                        if ( v128 )
                        {
                          vm->reg_flags = -128;
                          ++vm->reg_PC;
                          cycles_used = 1;
                        }
                        else
                        {
                          vm->reg_flags = 0;
                          ++vm->reg_PC;
                          cycles_used = 1;
                        }
                      }
                      break;
                    case 0xB8:
                      v181 = primary_opcode & 7;
                      if ( v181 == 6 )
                      {
                        do_compare(vm, vm->reg_A, memory_[*(_WORD *)&vm->reg_L], 0);
                        ++vm->reg_PC;
                        memory__ = vm->memory;
                        cycles_used = 2;
                      }
                      else
                      {
                        do_compare(
                          vm,
                          vm->reg_A,
                          *((_BYTE *)&vm->memory + register_byte_offsets[(unsigned __int64)v181]),
                          0);
                        ++vm->reg_PC;
                        memory__ = vm->memory;
                        cycles_used = 1;
                      }
                      break;
                    default:
                      if ( filtered_opcode == -57 )
                      {
                        v179 = vm->reg_PC + 1;
                        v180 = vm->reg_SP - 2;
                        vm->reg_SP = v180;
                        *(_WORD *)&memory_[(unsigned __int16)v180] = v179;
                        vm->reg_PC = primary_opcode & 0x38;
                        cycles_used = 4;
                      }
                      else if ( v171 == -63 )
                      {
                        v176 = vm->reg_SP;
                        v177 = (signed int)(primary_opcode & 0x30) >> 4;
                        if ( v177 == 3 )
                        {
                          v178 = vm->reg_SP;
                          *(_WORD *)&vm->reg_flags = *(_WORD *)&memory_[v176];
                          vm->reg_flags &= 0xF0u;
                        }
                        else
                        {
                          *(_WORD *)((char *)&vm->memory + register_word_offsets[v177]) = *(_WORD *)&memory_[v176];
                          v178 = vm->reg_SP;
                        }
                        ++vm->reg_PC;
                        cycles_used = 4;
                        vm->reg_SP = v178 + 2;
                      }
                      else
                      {
                        if ( v171 != 0xC5u )
                          goto GOODEXIT;
                        v173 = &vm->reg_flags;
                        v174 = (signed int)(primary_opcode & 0x30) >> 4;
                        if ( v174 != 3 )
                          v173 = (char *)&vm->memory + register_word_offsets[v174];
                        v175 = vm->reg_SP - 2;
                        vm->reg_SP = v175;
                        *(_WORD *)&memory_[(unsigned __int16)v175] = *(_WORD *)v173;
                        cycles_used = 4;
                        ++vm->reg_PC;
                      }
                      break;
                  }
                }
              }
              break;
          }
        }
        goto INSTR_DONE;
      case 0xCA:
        if ( vm->reg_flags < 0 )
        {
          cycles_used = 4;
          vm->reg_PC = *(_WORD *)(opcode_addr + 1);
        }
        else
        {
          cycles_used = 3;
          vm->reg_PC = temp_pc + 3;
        }
        goto INSTR_DONE;
      case 0xC9:
        v232 = *(_WORD *)&memory_[vm->reg_SP];
        vm->reg_SP += 2;
        vm->reg_PC = v232;
        cycles_used = 4;
        goto INSTR_DONE;
      case 0xC8:
        if ( vm->reg_flags < 0 )
        {
          v240 = *(_WORD *)&memory_[vm->reg_SP];
          vm->reg_SP += 2;
          vm->reg_PC = v240;
          cycles_used = 4;
        }
        else
        {
          cycles_used = 2;
          vm->reg_PC = temp_pc + 1;
        }
        goto INSTR_DONE;
      case 0xC6:
        v233 = opcode_addr[1];
        v234 = vm->reg_A;
        vm->reg_flags = 0;
        v235 = v234;
        v236 = v233 + v234;
        v237 = v233;
        if ( (_BYTE)v236 )
        {
          v238 = 16;
          v239 = 0;
        }
        else
        {
          vm->reg_flags = -128;
          v238 = -112;
          v239 = -128;
        }
        if ( v236 > 0xFFu )
        {
          vm->reg_flags = v238;
          v239 = v238;
        }
        if ( ((v235 & 0xF) + (v237 & 0xF)) & 0x10 )
          vm->reg_flags = v239 | 0x20;
        vm->reg_A = v236;
        cycles_used = 2;
        vm->reg_PC = temp_pc + 2;
        goto INSTR_DONE;
      case 0xC4:
        v241 = temp_pc + 3;
        v158 = vm->reg_flags < 0;
        cycles_used = 3;
        vm->reg_PC = v241;
        if ( !v158 )
        {
          v242 = *(_WORD *)(opcode_addr + 1);
          v243 = vm->reg_SP - 2;
          vm->reg_SP = v243;
          *(_WORD *)&memory_[(unsigned __int16)v243] = v241;
          vm->reg_PC = v242;
          cycles_used = 6;
        }
        goto INSTR_DONE;
      case 0xC3:
        cycles_used = 4;
        vm->reg_PC = *(_WORD *)(opcode_addr + 1);
        goto INSTR_DONE;
      case 0xC2:
        if ( vm->reg_flags < 0 )
        {
          cycles_used = 3;
          vm->reg_PC = temp_pc + 3;
        }
        else
        {
          cycles_used = 4;
          vm->reg_PC = *(_WORD *)(opcode_addr + 1);
        }
        goto INSTR_DONE;
      case 0xC0:
        if ( vm->reg_flags < 0 )
        {
          cycles_used = 2;
          vm->reg_PC = temp_pc + 1;
        }
        else
        {
          v244 = *(_WORD *)&memory_[vm->reg_SP];
          vm->reg_SP += 2;
          vm->reg_PC = v244;
          cycles_used = 4;
        }
        goto INSTR_DONE;
      case 0x76:
        vm->field_44 = 1;
        cycles_used = 1;
        vm->reg_PC = temp_pc + 1;
        goto INSTR_DONE;
      case 0x3F:
        v245 = vm->reg_flags;
        v246 = v245 & 0xFFFFFF9F | 0x10;
        if ( v245 & 0x10 )
          LOBYTE(v246) = vm->reg_flags & 0x8F;
        vm->reg_flags = v246;
        vm->reg_PC = temp_pc + 1;
        cycles_used = 1;
        goto INSTR_DONE;
      case 0x38:
        v247 = temp_pc + 2;
        v128 = (vm->reg_flags & 0x10) == 0;
        cycles_used = 2;
        vm->reg_PC = v247;
        if ( !v128 )
        {
          cycles_used = 3;
          vm->reg_PC = opcode_addr[1] + v247;
        }
        goto INSTR_DONE;
      case 0x37:
        v248 = vm->reg_flags;
        vm->reg_PC = temp_pc + 1;
        vm->reg_flags = v248 & 0x9F | 0x10;
        cycles_used = 1;
        goto INSTR_DONE;
      case 0x30:
        v249 = temp_pc + 2;
        v128 = (vm->reg_flags & 0x10) == 0;
        cycles_used = 2;
        vm->reg_PC = v249;
        if ( v128 )
        {
          cycles_used = 3;
          vm->reg_PC = opcode_addr[1] + v249;
        }
        goto INSTR_DONE;
      case 0x2F:
        vm->reg_A = ~vm->reg_A;
        vm->reg_flags |= 0x60u;
        vm->reg_PC = temp_pc + 1;
        cycles_used = 1;
        goto INSTR_DONE;
      case 0x28:
        v250 = temp_pc + 2;
        v158 = vm->reg_flags < 0;
        cycles_used = 2;
        vm->reg_PC = v250;
        if ( v158 )
        {
          cycles_used = 3;
          vm->reg_PC = opcode_addr[1] + v250;
        }
        goto INSTR_DONE;
      case 0x27:
        v251 = vm->reg_flags;
        if ( v251 & 0x40 )
        {
          if ( v251 & 0x20 )
          {
            v252 = vm->reg_A - 6;
            vm->reg_A = v252;
          }
          else
          {
            v252 = vm->reg_A;
          }
          if ( v251 & 0x10 )
          {
            v252 -= 96;
            vm->reg_A = v252;
          }
        }
        else
        {
          v254 = vm->reg_A;
          if ( (unsigned __int8)v254 > 0x99u || v251 & 0x10 )
          {
            v251 |= 0x10u;
            v255 = 102;
            v256 = 96;
          }
          else
          {
            v255 = 6;
            v256 = 0;
          }
          if ( (v254 & 0xFu) <= 9 && !(v251 & 0x20) )
            v255 = v256;
          v252 = v255 + v254;
          vm->reg_A = v252;
        }
        v253 = v251 & 0x5F;
        vm->reg_flags = v253;
        if ( !v252 )
          vm->reg_flags = v253 | 0x80;
        memory__ = memory_;
        cycles_used = 1;
        vm->reg_PC = temp_pc + 1;
        goto INSTR_DONE;
      case 0x20:
        v257 = temp_pc + 2;
        v158 = vm->reg_flags < 0;
        cycles_used = 2;
        vm->reg_PC = v257;
        if ( !v158 )
        {
          cycles_used = 3;
          vm->reg_PC = opcode_addr[1] + v257;
        }
        goto INSTR_DONE;
      case 0x1F:
        v258 = (unsigned __int8)vm->reg_A >> 1;
        v259 = -(vm->reg_A & 1);
        v260 = (vm->reg_flags & 0x10u) >= 1 ? 0xFFFFFF80 : 0;
        vm->reg_PC = temp_pc + 1;
        vm->reg_A = v260 | v258;
        vm->reg_flags = v259 & 0x10;
        cycles_used = 1;
        goto INSTR_DONE;
      case 0x18:
        v261 = temp_pc + 2;
        vm->reg_PC = v261;
        cycles_used = 3;
        vm->reg_PC = opcode_addr[1] + v261;
        goto INSTR_DONE;
      case 0x17:
        v262 = vm->reg_A;
        v263 = vm->reg_flags;
        vm->reg_PC = temp_pc + 1;
        v264 = 2 * v262 | (v263 >> 4) & 1;
        vm->reg_flags = ((char)v262 >> 7) & 0x10;
        cycles_used = 1;
        vm->reg_A = v264;
        goto INSTR_DONE;
      case 0x10:
        vm->reg_PC = temp_pc + 1;
        goto LABEL_232;
      case 0xF:
        v265 = vm->reg_A;
        vm->reg_PC = temp_pc + 1;
        vm->reg_flags = -(v265 & 1) & 0x10;
        cycles_used = 1;
        vm->reg_A = (v265 >> 1) | ((v265 & 1) << 7);
        goto INSTR_DONE;
      case 8:
        *(_WORD *)&memory_[*(_WORD *)(opcode_addr + 1)] = vm->reg_SP;
        cycles_used = 5;
        vm->reg_PC += 3;
        goto INSTR_DONE;
      case 7:
        v266 = vm->reg_A;
        vm->reg_PC = temp_pc + 1;
        v267 = __ROL1__(v266, 1);
        vm->reg_flags = (v266 >> 7) & 0x10;
        vm->reg_A = v267;
        cycles_used = 1;
        goto INSTR_DONE;
      case 0:
        cycles_used = 1;
        vm->reg_PC = temp_pc + 1;
        goto INSTR_DONE;
      default:
        filtered_opcode = primary_opcode & 0xC7;
        if ( (primary_opcode & 0xC7) == 2 )
        {
          v270 = &vm->reg_E;
          v271 = primary_opcode & 0x30;
          if ( (primary_opcode & 0x30) != 16 )
          {
            if ( v271 > 0x10u )
            {
              if ( v271 == 32 || v271 == 48 )
              {
                v270 = &vm->reg_L;
                goto LABEL_418;
              }
            }
            else
            {
              v270 = &vm->reg_C;
              if ( !v271 )
                goto LABEL_418;
            }
            v270 = 0LL;
          }
LABEL_418:
          if ( primary_opcode & 8 )
          {
            vm->reg_A = memory_[*(_WORD *)v270];
          }
          else
          {
            memory_[*(_WORD *)v270] = vm->reg_A;
            temp_pc = vm->reg_PC;
            memory__ = vm->memory;
          }
          if ( v271 == 32 )
          {
            ++*(_WORD *)&vm->reg_L;
          }
          else if ( v271 == 48 )
          {
            --*(_WORD *)&vm->reg_L;
          }
          cycles_used = 2;
          vm->reg_PC = temp_pc + 1;
          goto INSTR_DONE;
        }
        if ( filtered_opcode == 4 )
        {
          v278 = (signed int)(primary_opcode & 0x38) >> 3;
          if ( v278 == 6 )
            v279 = &memory_[*(_WORD *)&vm->reg_L];
          else
            v279 = (char *)&vm->memory + register_byte_offsets[v278];
          v280 = (*v279)++;
          v281 = vm->reg_flags & 0x1F;
          vm->reg_flags = v281;
          v282 = *v279;
          if ( !*v279 )
          {
            v281 |= 0x80u;
            vm->reg_flags = v281;
            v282 = *v279;
          }
          if ( ((unsigned __int8)v282 ^ (unsigned __int8)v280) & 0xF0 )
            vm->reg_flags = v281 | 0x20;
          ++vm->reg_PC;
          v128 = v278 == 6;
          memory__ = vm->memory;
          if ( v128 )
            cycles_used = 3;
          else
            cycles_used = 1;
        }
        else if ( filtered_opcode == 5 )
        {
          v272 = (signed int)(primary_opcode & 0x38) >> 3;
          if ( v272 == 6 )
            v273 = &memory_[*(_WORD *)&vm->reg_L];
          else
            v273 = (char *)&vm->memory + register_byte_offsets[v272];
          v274 = (*v273)--;
          v275 = vm->reg_flags & 0x1F;
          v276 = v275 | 0x40;
          vm->reg_flags = v275 | 0x40;
          v277 = *v273;
          if ( !*v273 )
          {
            v276 = v275 | 0xC0;
            vm->reg_flags = v275 | 0xC0;
            v277 = *v273;
          }
          if ( ((unsigned __int8)v277 ^ (unsigned __int8)v274) & 0xF0 )
            vm->reg_flags = v276 | 0x20;
          ++vm->reg_PC;
          v128 = v272 == 6;
          memory__ = vm->memory;
          if ( v128 )
            cycles_used = 3;
          else
            cycles_used = 1;
        }
        else
        {
          if ( filtered_opcode != 6 )
            goto COMPARE_REST;
          v268 = opcode_addr[1];
          v269 = (signed int)(primary_opcode & 0x38) >> 3;
          if ( v269 == 6 )
          {
            cycles_used = 3;
            memory_[*(_WORD *)&vm->reg_L] = v268;
            vm->reg_PC += 2;
            memory__ = vm->memory;
          }
          else
          {
            cycles_used = 2;
            *((_BYTE *)&vm->memory + register_byte_offsets[v269]) = v268;
            vm->reg_PC += 2;
            memory__ = vm->memory;
          }
        }
INSTR_DONE:
        vm->cycles_used = cycles_used;
        break;
    }
LABEL_18:
    somecounter = vm->somecounter + 1;
    vm->somecounter = somecounter;
    if ( somecounter == 109 )
    {
      vm->somecounter = 0;
    }
    else if ( somecounter )
    {
      if ( somecounter == 19 )
      {
        if ( memory__[0xFF44] > 143u )
          goto NO_SCREEN_DRAW;
        memory__[0xFF41] &= 0xFCu;
        vm->memory[0xFF41] |= 3u;
        goto LABEL_88;
      }
      if ( somecounter == 60 && memory__[0xFF44] <= 143u )
      {
        memory__[0xFF41] &= 0xFCu;
        memory__ = vm->memory;
        if ( vm->memory[0xFF41] & 8 )
        {
          memory__[0xFF0F] |= 2u;
          memory__ = vm->memory;
        }
      }
      goto NO_SCREEN_DRAW;
    }
    lcdc_y = memory__[0xFF44];
    if ( lcdc_y > 143u )
    {
      v68 = lcdc_y + 1;
      memory__[0xFF44] = v68;
      if ( v68 != 154 )
        goto LABEL_88;
      vm->memory[0xFF44] = 0;
    }
    else
    {
      v47 = lcdc_y + 1;
      memory__[0xFF44] = v47;
      if ( v47 == 144 )
      {
        v66 = vm->memory;
        vm->do_output = 1;
        v66[65345] &= 0xFCu;
        vm->memory[65345] |= 1u;
        v67 = vm->memory;
        if ( vm->memory[65345] & 0x10 )
        {
          v67[65295] |= 2u;
          v67 = vm->memory;
        }
        v67[65295] |= 1u;
        memory__ = vm->memory;
        goto NO_SCREEN_DRAW;
      }
    }
    vm->memory[0xFF41] &= 0xFCu;
    vm->memory[0xFF41] |= 2u;
    v48 = vm->memory;
    v49 = vm->memory[0xFF41];
    if ( v49 & 0x20 )
    {
      v48[0xFF0F] |= 2u;
      v48 = vm->memory;
      v49 = vm->memory[0xFF41];
    }
    v48[0xFF41] = v49 & 0xFB;
    memory__ = vm->memory;
    if ( vm->memory[0xFF44] == vm->memory[0xFF45] )
    {
      memory__[0xFF41] |= 4u;
      memory__ = vm->memory;
      if ( vm->memory[0xFF41] & 0x40 )
      {
        memory__[0xFF0F] |= 2u;
        memory__ = vm->memory;
      }
    }
    v50 = memory__[0xFF47];
    vm->bg_pal_0 = memory__[0xFF47] & 3;
    vm->bg_pal_1 = (v50 & 0xC) >> 2;
    vm->bg_pal_3 = v50 >> 6;
    vm->bg_pal_2 = (v50 & 0x30) >> 4;
    v51 = memory__[0xFF48];
    vm->ob0_pal_0 = memory__[0xFF48] & 3;
    vm->ob0_pal_1 = (v51 & 0xC) >> 2;
    vm->ob0_pal_3 = v51 >> 6;
    vm->ob0_pal_2 = (v51 & 0x30) >> 4;
    v52 = memory__[0xFF49];
    vm->ob1_pal_0 = memory__[0xFF49] & 3;
    vm->ob1_pal_1 = (v52 & 0xC) >> 2;
    vm->ob1_pal_3 = v52 >> 6;
    vm->ob1_pal_2 = (v52 & 0x30) >> 4;
    mem_FF40_LCDC = memory__[0xFF40];
    mem_FF44_LY = memory__[0xFF44];
    if ( mem_FF40_LCDC & 1 )
    {
      mem_bgmap = memory__ + 0x9800;
      if ( mem_FF40_LCDC & 8 )
        mem_bgmap = memory__ + 0x9C00;
      v56 = 0LL;
      while ( 1 )
      {
        mem_bgmap_indexer = mem_bgmap;
        v58 = v56;
        memory___ = memory__;
        v60 = *mem_bgmap;
        if ( mem_FF40_LCDC & 0x10 )
        {
LABEL_77:
          v61 = &memory___[0x10 * ((unsigned __int8)v60 + 0x800)];
          goto LABEL_78;
        }
        while ( 1 )
        {
          v61 = &memory___[0x10 * (v60 + 0x900)];
LABEL_78:
          v62 = &vm->window_memory[v58];
          v63 = v62 + 0x800;
          do
          {
            *v62 = *(&vm->bg_pal_0 + (((unsigned int)(char)*v61 >> 31) | ((v61[1] & 0x80u) >= 1 ? 2 : 0)));
            v62[1] = *(&vm->bg_pal_0 + ((*v61 >> 6) & 1 | ((unsigned int)v61[1] >> 5) & 2));
            v62[2] = *(&vm->bg_pal_0 + ((*v61 >> 5) & 1 | ((unsigned int)v61[1] >> 4) & 2));
            v62[3] = *(&vm->bg_pal_0 + ((*v61 >> 4) & 1 | ((unsigned int)v61[1] >> 3) & 2));
            v62[4] = *(&vm->bg_pal_0 + ((*v61 >> 3) & 1 | ((unsigned int)v61[1] >> 2) & 2));
            v62[5] = *(&vm->bg_pal_0 + ((*v61 >> 2) & 1 | ((unsigned int)v61[1] >> 1) & 2));
            v62[6] = *(&vm->bg_pal_0 + ((*v61 >> 1) & 1 | v61[1] & 2u));
            v64 = *v61 & 1;
            v65 = 2 * v61[1];
            v62 += 256;
            v61 += 2;
            *(v62 - 249) = *(&vm->bg_pal_0 + (v64 | v65 & 2u));
          }
          while ( v62 != v63 );
          v58 += 8LL;
          ++mem_bgmap_indexer;
          if ( v58 == v56 + 256 )
            break;
          memory___ = vm->memory;
          v60 = *mem_bgmap_indexer;
          if ( vm->memory[0xFF40] & 0x10 )
            goto LABEL_77;
        }
        v56 += 2048LL;
        mem_bgmap += 32;
        if ( v56 == 0x10000 )
          break;
        memory__ = vm->memory;
        mem_FF40_LCDC = vm->memory[0xFF40];
      }
      v73 = 0LL;
      v74 = vm->memory[0xFF43];
      v75 = (unsigned __int8)(vm->memory[0xFF42] + mem_FF44_LY) << 8;
      do
      {
        v76 = *(&vm->window_memory[v75] + (unsigned __int8)(v74 + v73));
        v77 = vm->video_memory + v73++;
        *(_BYTE *)(v77 + 160 * mem_FF44_LY) = v76;
      }
      while ( v73 != 160 );
LABEL_88:
      memory__ = vm->memory;
    }
NO_SCREEN_DRAW:
    if ( memory__[0xFF46] != 0xFFu )
    {
      dest = vm->dma_destination;
      src = &memory__[(memory__[0xFF46] << 8) & 0xFF00];
      *(_QWORD *)dest = *(_QWORD *)src;
      *((_QWORD *)dest + 19) = *((_QWORD *)src + 19);
      qmemcpy(
        (void *)(((unsigned __int64)dest + 8) & 0xFFFFFFFFFFFFFFF8LL),
        (const void *)((_BYTE *)src - ((char *)dest - (((unsigned __int64)dest + 8) & 0xFFFFFFFFFFFFFFF8LL))),
        8LL * (((unsigned int)dest - (((_DWORD)dest + 8) & 0xFFFFFFF8) + 0xA0) >> 3));
      vm->memory[0xFF46] = 0xFFu;
      memory__ = vm->memory;
    }
    v25 = vm->field_5C + 1;
    vm->field_5C = v25;
    if ( v25 == 61 )
    {
      ++memory__[0xFF04];
      vm->field_5C = 0;
      memory__ = vm->memory;
    }
    v26 = memory__[0xFF07];
    if ( v26 & 4 )
    {
      v27 = v26 & 3;
      v28 = 15;
      if ( v27 != 2 )
      {
        LOBYTE(v28) = 61;
        if ( v27 != 3 )
        {
          LOBYTE(v28) = -12;
          if ( v27 == 1 )
            v28 = 4;
        }
      }
      v29 = vm->field_60 + 1;
      vm->field_60 = v29;
      if ( v29 >= (unsigned int)v28 )
      {
        vm->field_60 = 0;
        v30 = memory__[0xFF05];
        memory__[0xFF05] = v30 + 1;
        if ( v30 == -1 )
        {
          vm->memory[0xFF05] = vm->memory[0xFF06];
          vm->memory[0xFF0F] |= 4u;
        }
      }
    }
    if ( vm->do_output )
    {
      ++v14;
      if ( v14 == 10 * (v14 / 0xA) && vm->memory[0xFF40] < 0 )
      {
        v78 = 160LL;
        printf("\x1B[H");
        do
        {
          v79 = v78 - 160;
          do
          {
            v80 = vm->video_memory + v79;
            v81 = (*(_BYTE *)(v80 + 320) >= 1u ? 4 : 0) | (*(_BYTE *)(v80 + 160) >= 1u ? 2 : 0) | (*(_BYTE *)v80 != 0);
            v82 = *(_BYTE *)(v80 + 1) < 1u;
            outputstring[0] = 0xE2u;
            outputstring[1] = 0xA0u;
            outputstring[3] = 0;
            v79 += 2LL;
            outputstring[2] = ((*(_BYTE *)(v80 + 161) >= 1u ? 0x10 : 0) | ~-v82 & 8 | v81 | (*(_BYTE *)(v80 + 321) >= 1u ? 0x20 : 0))
                            + 0x80;
            printf("%s", outputstring);
          }
          while ( v79 != v78 );
          v78 = v79 + 480;
          putchar('\n');
        }
        while ( v79 != 22720 );
        putchar('\n');
      }
      vm->do_output = 0;
      fflush(stdout);
    }
    if ( (long double)v15 == 2000.0 * vm->field_48 )
    {
      v15 = 0;
      usleep(10000u);
      vm->joy_input = 0;
    }
    else
    {
      ++v15;
    }
    v9 = v31;
  }
GOODEXIT:
  printf("\x1B[?25h");
  return 0LL;
}