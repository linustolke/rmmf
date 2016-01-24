# rmmf
Read Multiple MakeFiles
## Restrictions version 1
* One level transformations only
* All transformed targets on the top level are .PHONY
* All transformed targets on the lower level can only have a single use on the top level
## Transforms
makefile:
```
.PHONY: goal1
goal1: dep1 dep2
	cd dir1 && make goal11
goal2: goal1
...
```
dir1/makefile:
```
goal11 : dep
	command11
```

transforms to:
```
.PHONY: goal1
.PHONY: goal1_deps
goal1 : goal1_deps dir1/goal11
dep: goal1_deps
dir1/goal11 : goal1_deps dep
	cd dir1 && command11
```
