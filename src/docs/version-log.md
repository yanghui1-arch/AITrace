# Version log
Every version updates, fixes and removings could be checked here.
## 0.1.4
### Feature
- Add PatchResponse as a standard output but not make influences on callers. - by @yanghui1-arch [(65f3e25)](https://github.com/yanghui1-arch/mwin/commit/65f3e254119a8ef84bffe0079dcbede8e0b1209a)

### Fix
- Fix serialization custom instance function inputs bug - by @yanghui1-arch [(a11eca5)](https://github.com/yanghui1-arch/mwin/commit/a11eca50ead7e047dabe05ea219cd7bfcca4e450)
- Fix AITraceConfig name bug and rename AITraceConfig, AITraceConfigurator to MwinConfig, MwinConfigurator - by @yanghui1-arch [(c53c7d5)](https://github.com/yanghui1-arch/mwin/commit/c53c7d5d82ac3174328de866b8e06ba66917bc87)
- Fix step and trace time format - by @yanghui1-arch [(f43de40)](https://github.com/yanghui1-arch/mwin/commit/f43de40493f1a66813263bbdc73e521ccaf154df)

### Remove
- Remove useless print statements - by @yanghui1-arch [(681fbec)](https://github.com/yanghui1-arch/mwin/commit/681fbecbb6c04fd328b759627cb5871f6cbc1975)
- Remove useless codes in inspect_helper - by @yanghui1-arch [(eabe438)](https://github.com/yanghui1-arch/mwin/commit/eabe438194d43660dc15f590ee052e47eba6d1fc)
- Replace stream.py to std.py - by @yanghui1-arch [(2de1e36)](https://github.com/yanghui1-arch/mwin/commit/2de1e365b179173ae6851663249c9ad565c950e0)
- Remove openai extra output in sync, async and stream, no-stream mode - by @yanghui1-arch [(b02743b)](https://github.com/yanghui1-arch/mwin/commit/b02743b88b81078a0ed6d492053e4947b6523eb0) [(88f9682)](https://github.com/yanghui1-arch/mwin/commit/88f968277e2c4870b102b43757311c7d443d89c7) [(b898e83)](https://github.com/yanghui1-arch/mwin/commit/b898e83f35269f847a2b249871b92aed1a194090)