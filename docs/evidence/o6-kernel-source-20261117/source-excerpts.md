# Utdrag fra Ubuntu linux 7.0.0-43.43

Hentet og avstemt 2026-11-17. Linjenumre gjelder rekonstruert kilde. Utdrag er lesekopier; filhashene gjelder de komplette lokalt utpakkede filene. Ikke kjørte tester eller ny servermåling.

## drivers/android/binder_alloc.h

```text
108: struct binder_alloc {
109: 	struct mutex mutex;
110: 	struct mm_struct *mm;
111: 	unsigned long vm_start;
112: 	struct list_head buffers;
113: 	struct rb_root free_buffers;
114: 	struct rb_root allocated_buffers;
115: 	size_t free_async_space;
116: 	struct page **pages;
117: 	struct list_lru *freelist;
118: 	size_t buffer_size;
119: 	int pid;
120: 	size_t pages_high;
121: 	bool mapped;
122: 	bool oneway_spam_detected;
123: };
```

## drivers/android/binder_alloc.c

```text
253: static int binder_page_insert(struct binder_alloc *alloc,
254: 			      unsigned long addr,
255: 			      struct page *page)
256: {
257: 	struct mm_struct *mm = alloc->mm;
258: 	struct vm_area_struct *vma;
259: 	int ret = -ESRCH;
260:
261: 	/* attempt per-vma lock first */
262: 	vma = lock_vma_under_rcu(mm, addr);
263: 	if (vma) {
264: 		if (binder_alloc_is_mapped(alloc))
265: 			ret = vm_insert_page(vma, addr, page);
266: 		vma_end_read(vma);
267: 		return ret;
268: 	}
269:
270: 	/* fall back to mmap_lock */
271: 	mmap_read_lock(mm);
272: 	vma = vma_lookup(mm, addr);
273: 	if (vma && binder_alloc_is_mapped(alloc))
274: 		ret = vm_insert_page(vma, addr, page);
275: 	mmap_read_unlock(mm);
276:
277: 	return ret;
278: }
912: 	alloc->buffer_size = min_t(unsigned long, vma->vm_end - vma->vm_start,
913: 				   SZ_4M);
914: 	mutex_unlock(&binder_alloc_mmap_lock);
915:
916: 	alloc->vm_start = vma->vm_start;
917:
918: 	alloc->pages = kvzalloc_objs(alloc->pages[0],
919: 				     alloc->buffer_size / PAGE_SIZE);
920: 	if (!alloc->pages) {
921: 		ret = -ENOMEM;
922: 		failure_string = "alloc page array";
1110: /**
1111:  * binder_alloc_vma_close() - invalidate address space
1112:  * @alloc: binder_alloc for this proc
1113:  *
1114:  * Called from binder_vma_close() when releasing address space.
1115:  * Clears alloc->mapped to prevent new incoming transactions from
1116:  * allocating more buffers.
1117:  */
1118: void binder_alloc_vma_close(struct binder_alloc *alloc)
1119: {
1120: 	binder_alloc_set_mapped(alloc, false);
1121: }
1133: enum lru_status binder_alloc_free_page(struct list_head *item,
1134: 				       struct list_lru_one *lru,
1135: 				       void *cb_arg)
1136: 	__must_hold(&lru->lock)
1137: {
1138: 	struct binder_shrinker_mdata *mdata = container_of(item, typeof(*mdata), lru);
1139: 	struct binder_alloc *alloc = mdata->alloc;
1140: 	struct mm_struct *mm = alloc->mm;
1141: 	struct vm_area_struct *vma;
1142: 	struct page *page_to_free;
1143: 	unsigned long page_addr;
1144: 	int mm_locked = 0;
1145: 	size_t index;
1146:
1147: 	if (!mmget_not_zero(mm))
1148: 		goto err_mmget;
1149:
1150: 	index = mdata->page_index;
1151: 	page_addr = alloc->vm_start + index * PAGE_SIZE;
1152:
1153: 	/* attempt per-vma lock first */
1154: 	vma = lock_vma_under_rcu(mm, page_addr);
1155: 	if (!vma) {
1156: 		/* fall back to mmap_lock */
1157: 		if (!mmap_read_trylock(mm))
1158: 			goto err_mmap_read_lock_failed;
1159: 		mm_locked = 1;
1160: 		vma = vma_lookup(mm, page_addr);
1161: 	}
1162:
1163: 	if (!mutex_trylock(&alloc->mutex))
1164: 		goto err_get_alloc_mutex_failed;
1165:
1166: 	/*
1167: 	 * Since a binder_alloc can only be mapped once, we ensure
1168: 	 * the vma corresponds to this mapping by checking whether
1169: 	 * the binder_alloc is still mapped.
1170: 	 */
1171: 	if (vma && !binder_alloc_is_mapped(alloc))
1172: 		goto err_invalid_vma;
1173:
1174: 	trace_binder_unmap_kernel_start(alloc, index);
1175:
1176: 	page_to_free = alloc->pages[index];
1177: 	binder_set_installed_page(alloc, index, NULL);
1178:
1179: 	trace_binder_unmap_kernel_end(alloc, index);
1180:
1181: 	list_lru_isolate(lru, item);
1182: 	spin_unlock(&lru->lock);
1183:
1184: 	if (vma) {
1185: 		trace_binder_unmap_user_start(alloc, index);
1186:
1187: 		zap_page_range_single(vma, page_addr, PAGE_SIZE, NULL);
1188:
1189: 		trace_binder_unmap_user_end(alloc, index);
1190: 	}
1191:
1192: 	mutex_unlock(&alloc->mutex);
1193: 	if (mm_locked)
1194: 		mmap_read_unlock(mm);
1195: 	else
1196: 		vma_end_read(vma);
1197: 	mmput_async(mm);
1198: 	binder_free_page(page_to_free);
1199:
1200: 	return LRU_REMOVED_RETRY;
1201:
1202: err_invalid_vma:
1203: 	mutex_unlock(&alloc->mutex);
1204: err_get_alloc_mutex_failed:
1205: 	if (mm_locked)
1206: 		mmap_read_unlock(mm);
1207: 	else
1208: 		vma_end_read(vma);
1209: err_mmap_read_lock_failed:
1210: 	mmput_async(mm);
```

## fs/Kconfig

```text
61: 	depends on ZONE_DEVICE
94: 	depends on ZONE_DEVICE
155: source "fs/ntfs3/Kconfig"
```

## fs/Makefile

```text
93: obj-$(CONFIG_NTFS3_FS)		+= ntfs3/
```

## fs/ntfs3/Kconfig

```text
1: # SPDX-License-Identifier: GPL-2.0-only
2: config NTFS3_FS
3: 	tristate "NTFS Read-Write file system support"
4: 	select BUFFER_HEAD
5: 	select NLS
6: 	select LEGACY_DIRECT_IO
7: 	help
8: 	  Windows OS native file system (NTFS) support up to NTFS version 3.1.
9:
10: 	  Y or M enables the NTFS3 driver with full features enabled (read,
11: 	  write, journal replaying, sparse/compressed files support).
12: 	  File system type to use on mount is "ntfs3". Module name (M option)
13: 	  is also "ntfs3".
14:
15: 	  Documentation: <file:Documentation/filesystems/ntfs3.rst>
16:
17: config NTFS3_64BIT_CLUSTER
```

## kernel/bpf/arraymap.c

```text
60: 	    attr->value_size == 0 ||
61: 	    attr->map_flags & ~ARRAY_CREATE_FLAG_MASK ||
62: 	    !bpf_map_flags_access_ok(attr->map_flags) ||
63: 	    (percpu && numa_node != NUMA_NO_NODE))
64: 		return -EINVAL;
65:
66: 	if (attr->map_type != BPF_MAP_TYPE_ARRAY &&
67: 	    attr->map_flags & (BPF_F_MMAPABLE | BPF_F_INNER_MAP))
68: 		return -EINVAL;
265: static int percpu_array_map_gen_lookup(struct bpf_map *map, struct bpf_insn *insn_buf)
266: {
267: 	struct bpf_array *array = container_of(map, struct bpf_array, map);
268: 	struct bpf_insn *insn = insn_buf;
269:
270: 	if (!bpf_jit_supports_percpu_insn())
271: 		return -EOPNOTSUPP;
272:
273: 	if (map->map_flags & BPF_F_INNER_MAP)
274: 		return -EOPNOTSUPP;
275:
276: 	BUILD_BUG_ON(offsetof(struct bpf_array, map) != 0);
277: 	*insn++ = BPF_ALU64_IMM(BPF_ADD, BPF_REG_1, offsetof(struct bpf_array, pptrs));
278:
279: 	*insn++ = BPF_LDX_MEM(BPF_W, BPF_REG_0, BPF_REG_2, 0);
280: 	if (!map->bypass_spec_v1) {
281: 		*insn++ = BPF_JMP_IMM(BPF_JGE, BPF_REG_0, map->max_entries, 6);
282: 		*insn++ = BPF_ALU32_IMM(BPF_AND, BPF_REG_0, array->index_mask);
283: 	} else {
284: 		*insn++ = BPF_JMP_IMM(BPF_JGE, BPF_REG_0, map->max_entries, 5);
285: 	}
286:
287: 	*insn++ = BPF_ALU64_IMM(BPF_LSH, BPF_REG_0, 3);
288: 	*insn++ = BPF_ALU64_REG(BPF_ADD, BPF_REG_0, BPF_REG_1);
289: 	*insn++ = BPF_LDX_MEM(BPF_DW, BPF_REG_0, BPF_REG_0, 0);
290: 	*insn++ = BPF_MOV64_PERCPU_REG(BPF_REG_0, BPF_REG_0);
595: static bool array_map_meta_equal(const struct bpf_map *meta0,
596: 				 const struct bpf_map *meta1)
597: {
598: 	if (!bpf_map_meta_equal(meta0, meta1))
599: 		return false;
600: 	return meta0->map_flags & BPF_F_INNER_MAP ? true :
601: 	       meta0->max_entries == meta1->max_entries;
602: }
830: const struct bpf_map_ops percpu_array_map_ops = {
831: 	.map_meta_equal = bpf_map_meta_equal,
832: 	.map_alloc_check = array_map_alloc_check,
833: 	.map_alloc = array_map_alloc,
834: 	.map_free = array_map_free,
835: 	.map_get_next_key = bpf_array_get_next_key,
836: 	.map_lookup_elem = percpu_array_map_lookup_elem,
837: 	.map_gen_lookup = percpu_array_map_gen_lookup,
838: 	.map_update_elem = array_map_update_elem,
839: 	.map_delete_elem = array_map_delete_elem,
```

## kernel/bpf/map_in_map.c

```text
84: bool bpf_map_meta_equal(const struct bpf_map *meta0,
85: 			const struct bpf_map *meta1)
86: {
87: 	/* No need to compare ops because it is covered by map_type */
88: 	return meta0->map_type == meta1->map_type &&
89: 		meta0->key_size == meta1->key_size &&
90: 		meta0->value_size == meta1->value_size &&
91: 		meta0->map_flags == meta1->map_flags &&
92: 		btf_record_equal(meta0->record, meta1->record);
93: }
```

## arch/x86/net/bpf_jit_comp.c

```text
3981: bool bpf_jit_supports_percpu_insn(void)
3982: {
3983: 	return true;
3984: }
```

## drivers/gpu/drm/amd/amdgpu/Makefile

```text
270: # add gfx usermode queue
271: amdgpu-y += amdgpu_userq.o
```

## drivers/gpu/drm/amd/amdgpu/amdgpu_userq.c

```text
879: 	}
880:
881: 	r = uq_funcs->mqd_create(queue, &args->in);
882: 	if (r) {
883: 		drm_file_err(uq_mgr->file, "Failed to create Queue\n");
884: 		amdgpu_userq_fence_driver_free(queue);
885: 		kfree(queue);
886: 		goto unlock;
887: 	}
888:
889: 	/* drop this refcount during queue destroy */
890: 	kref_init(&queue->refcount);
891:
892: 	/* Wait for mode-1 reset to complete */
893: 	down_read(&adev->reset_domain->sem);
894: 	r = xa_err(xa_store_irq(&adev->userq_doorbell_xa, index, queue, GFP_KERNEL));
895: 	if (r) {
896: 		kfree(queue);
897: 		up_read(&adev->reset_domain->sem);
898: 		goto unlock;
899: 	}
```

## drivers/gpu/drm/drm_pagemap.c

```text
728: 		order = folio_order(page_folio(src_page));
729:
730: 		/* TODO: Support fallback to single pages if THP allocation fails */
731: 		if (vas)
732: 			folio = vma_alloc_folio(GFP_HIGHUSER, order, vas, addr);
733: 		else
734: 			folio = folio_alloc(GFP_HIGHUSER, order);
735:
736: 		if (!folio)
737: 			goto free_pages;
738:
739: 		page = folio_page(folio, 0);
740: 		mpfn[i] = migrate_pfn(page_to_pfn(page));
741:
742: next:
743: 		if (page)
744: 			addr += page_size(page);
745: 		else
746: 			addr += PAGE_SIZE;
747:
748: 		i += NR_PAGES(order);
749: 	}
769: free_pages:
770: 	for (i = 0; i < npages;) {
771: 		struct page *page = migrate_pfn_to_page(mpfn[i]);
772: 		unsigned int order = 0;
773:
774: 		if (!page)
775: 			goto next_put;
776:
777: 		put_page(page);
778: 		mpfn[i] = 0;
779:
780: 		order = folio_order(page_folio(page));
781:
782: next_put:
783: 		i += NR_PAGES(order);
784: 	}
785: 	return -ENOMEM;
```

## drivers/gpu/drm/Makefile

```text
109: drm_gpusvm_helper-y := \
110: 	drm_gpusvm.o
111: drm_gpusvm_helper-$(CONFIG_ZONE_DEVICE) += \
112: 	drm_pagemap.o\
113: 	drm_pagemap_util.o
115: obj-$(CONFIG_DRM_GPUSVM) += drm_gpusvm_helper.o
```

## fs/smb/server/mgmt/user_session.c

```text
419: static void ksmbd_expire_session(struct ksmbd_conn *conn)
420: {
421: 	unsigned long id;
422: 	struct ksmbd_session *sess;
423:
424: 	down_write(&sessions_table_lock);
425: 	down_write(&conn->session_lock);
426: 	xa_for_each(&conn->sessions, id, sess) {
427: 		if (atomic_read(&sess->refcnt) <= 1 &&
428: 		    (sess->state != SMB2_SESSION_VALID ||
429: 		     time_after(jiffies,
430: 			       sess->last_active + SMB2_SESSION_TIMEOUT))) {
431: 			xa_erase(&conn->sessions, sess->id);
432: 			ksmbd_session_remove_from_table(sess);
433: 			ksmbd_session_destroy(sess);
434: 			continue;
435: 		}
436: 	}
437: 	up_write(&conn->session_lock);
438: 	up_write(&sessions_table_lock);
439: }
440:
441: int ksmbd_session_register(struct ksmbd_conn *conn,
442: 			   struct ksmbd_session *sess)
443: {
444: 	int ret;
445:
446: 	sess->dialect = conn->dialect;
447: 	memcpy(sess->ClientGUID, conn->ClientGUID, SMB2_CLIENT_GUID_SIZE);
448: 	ksmbd_expire_session(conn);
449: 	ret = xa_err(xa_store(&conn->sessions, sess->id, sess,
450: 			      KSMBD_DEFAULT_GFP));
```

## fs/smb/server/smb2pdu.h

```text
60: #define SMB2_SESSION_EXPIRED		(0)
61: #define SMB2_SESSION_IN_PROGRESS	BIT(0)
62: #define SMB2_SESSION_VALID		BIT(1)
63:
64: #define SMB2_SESSION_TIMEOUT		(10 * HZ)
65:
66: /* Apple Defined Contexts */
```

## debian.master/changelog

```text
1: linux (7.0.0-43.43) resolute; urgency=medium
2:
3:   * resolute/linux: 7.0.0-43.43 -proposed tracker (LP: #2171676)
4:
```
