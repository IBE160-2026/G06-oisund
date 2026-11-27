# Ubuntu linux 7.0.0-44.44: relevante kodevilkår

Rekonstruert fra hashkontrollert Ubuntu-kilde 27. november 2026. Linjenumre gjelder denne kilden; dette er ikke en servermåling.

## kernel/bpf/arraymap.c

```text
830: const struct bpf_map_ops percpu_array_map_ops = {
831: 	.map_meta_equal = bpf_map_meta_equal,
832: 	.map_alloc_check = array_map_alloc_check,
833: 	.map_alloc = array_map_alloc,
834: 	.map_free = array_map_free,
835: 	.map_get_next_key = bpf_array_get_next_key,
836: 	.map_lookup_elem = percpu_array_map_lookup_elem,
837: 	.map_gen_lookup = percpu_array_map_gen_lookup,
838: 	.map_update_elem = array_map_update_elem,
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

## drivers/gpu/drm/amd/amdgpu/amdgpu_userq.c

```text
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
64: #define SMB2_SESSION_TIMEOUT		(10 * HZ)
```
