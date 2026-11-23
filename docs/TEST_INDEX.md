# B-Tests archive and test index

This index covers the repository's test code, experiment runners, fixtures, retained
results, and proposed comparisons. Use the linked records to determine which cases ran,
on which revision, and under which conditions.

[What was compared](COMPARISON_SCOPE.md) · [AI entry point (JSON)](../research/test-index.json) · [Full file inventory (JSONL)](../research/test-inventory.jsonl) · [Generator](../tools/build_test_index.py) · [Update workflow](https://github.com/mitchell-d00/B-Tests/actions/workflows/test-index.yml)

Found **190 Python test definitions** in **21 files**, **1236 repository files** and **11 archives** with **2077 listed member files**.
Case records may include repeated trials, references, and unrun cases.

## Automated test definitions

The count comes from source definitions. Runtime discovery can differ for generated or parameterized tests.
Run the main suite with `python -m unittest discover -s tests -q`. Run the Witness package
suite from `evaluation/witness-section19/research-archive` with the same command.

| Test source | Definitions |
| --- | ---: |
| [evaluation/witness-section19/research-archive/tests/test_separation.py](../evaluation/witness-section19/research-archive/tests/test_separation.py) | 16 |
| [evaluation/witness-section19/research-archive/tests/test_wie.py](../evaluation/witness-section19/research-archive/tests/test_wie.py) | 26 |
| [tests/test_blind_handoff.py](../tests/test_blind_handoff.py) | 6 |
| [tests/test_cad_reference.py](../tests/test_cad_reference.py) | 38 |
| [tests/test_comparison_scope.py](../tests/test_comparison_scope.py) | 3 |
| [tests/test_critical_bench.py](../tests/test_critical_bench.py) | 7 |
| [tests/test_discovery_bench.py](../tests/test_discovery_bench.py) | 3 |
| [tests/test_human_export_bench.py](../tests/test_human_export_bench.py) | 3 |
| [tests/test_independent_audit.py](../tests/test_independent_audit.py) | 9 |
| [tests/test_kill_harness.py](../tests/test_kill_harness.py) | 18 |
| [tests/test_native_evidence.py](../tests/test_native_evidence.py) | 3 |
| [tests/test_oocc_correction.py](../tests/test_oocc_correction.py) | 4 |
| [tests/test_paired.py](../tests/test_paired.py) | 13 |
| [tests/test_propagation_bench.py](../tests/test_propagation_bench.py) | 3 |
| [tests/test_public_claims.py](../tests/test_public_claims.py) | 7 |
| [tests/test_runner_subprocess.py](../tests/test_runner_subprocess.py) | 4 |
| [tests/test_score_scaling.py](../tests/test_score_scaling.py) | 10 |
| [tests/test_sorter_random_batches.py](../tests/test_sorter_random_batches.py) | 2 |
| [tests/test_test_index.py](../tests/test_test_index.py) | 1 |
| [tests/test_witness_live.py](../tests/test_witness_live.py) | 6 |
| [tests/test_witness_separation.py](../tests/test_witness_separation.py) | 8 |

<details>
<summary>Browse individual Python tests</summary>

**[evaluation/witness-section19/research-archive/tests/test_separation.py](../evaluation/witness-section19/research-archive/tests/test_separation.py)**

- [TestParse.test_labels](../evaluation/witness-section19/research-archive/tests/test_separation.py#L59)
- [TestSeparationEffect.test_graded_improvement_supports](../evaluation/witness-section19/research-archive/tests/test_separation.py#L66)
- [TestSeparationEffect.test_flat_performance_weakens](../evaluation/witness-section19/research-archive/tests/test_separation.py#L75)
- [TestSeparationEffect.test_reversed_order_weakens](../evaluation/witness-section19/research-archive/tests/test_separation.py#L84)
- [TestSeparationEffect.test_stricter_is_not_better](../evaluation/witness-section19/research-archive/tests/test_separation.py#L91)
- [TestSeparationEffect.test_reject_all_scores_like_accept_all](../evaluation/witness-section19/research-archive/tests/test_separation.py#L102)
- [TestSeparationEffect.test_evidence_not_separation](../evaluation/witness-section19/research-archive/tests/test_separation.py#L109)
- [TestSeparationEffect.test_mixed_when_only_one_mode_shows_effect](../evaluation/witness-section19/research-archive/tests/test_separation.py#L121)
- [TestSeparationEffect.test_abstain_counts_against_overall_judgment](../evaluation/witness-section19/research-archive/tests/test_separation.py#L129)
- [TestSeparationEffect.test_permutation_is_deterministic](../evaluation/witness-section19/research-archive/tests/test_separation.py#L136)
- [TestSeparationEffect.test_single_level_is_not_run](../evaluation/witness-section19/research-archive/tests/test_separation.py#L143)
- [TestSeparationEffect.test_refuses_tampered_run](../evaluation/witness-section19/research-archive/tests/test_separation.py#L148)
- [TestSeparationEffect.test_writes_report](../evaluation/witness-section19/research-archive/tests/test_separation.py#L156)
- [TestFalseSupportRate.test_no_effect_rarely_reported_as_support](../evaluation/witness-section19/research-archive/tests/test_separation.py#L166)
- [TestDeterministicJudgesOnDemo.test_deterministic_stratum_is_flagged_as_confounded](../evaluation/witness-section19/research-archive/tests/test_separation.py#L182)
- [TestAbstentionMetrics.test_abstention_reduces_accuracy_and_coverage_without_a_false_alarm](../evaluation/witness-section19/research-archive/tests/test_separation.py#L194)

**[evaluation/witness-section19/research-archive/tests/test_wie.py](../evaluation/witness-section19/research-archive/tests/test_wie.py)**

- [TestGenerate.test_balanced_and_complete](../evaluation/witness-section19/research-archive/tests/test_wie.py#L29)
- [TestGenerate.test_same_seed_same_bytes](../evaluation/witness-section19/research-archive/tests/test_wie.py#L36)
- [TestGenerate.test_different_seed_differs](../evaluation/witness-section19/research-archive/tests/test_wie.py#L43)
- [TestGenerate.test_refuses_to_overwrite](../evaluation/witness-section19/research-archive/tests/test_wie.py#L48)
- [TestGenerate.test_generated_cases_have_no_synthetic_self_assessment](../evaluation/witness-section19/research-archive/tests/test_wie.py#L52)
- [TestGenerate.test_every_case_has_all_records](../evaluation/witness-section19/research-archive/tests/test_wie.py#L59)
- [TestNoLeak.test_key_facts_not_in_case_files_or_exports](../evaluation/witness-section19/research-archive/tests/test_wie.py#L66)
- [TestNoLeak.test_i0_export_labels_generated_records_as_a_proxy](../evaluation/witness-section19/research-archive/tests/test_wie.py#L78)
- [TestNoLeak.test_packet_and_report_do_not_reveal_staleness](../evaluation/witness-section19/research-archive/tests/test_wie.py#L85)
- [TestNoLeak.test_record_shapes_are_identical_across_classes](../evaluation/witness-section19/research-archive/tests/test_wie.py#L92)
- [TestFreeze.test_verify_clean](../evaluation/witness-section19/research-archive/tests/test_wie.py#L102)
- [TestFreeze.test_case_tamper_detected](../evaluation/witness-section19/research-archive/tests/test_wie.py#L105)
- [TestFreeze.test_key_tamper_detected](../evaluation/witness-section19/research-archive/tests/test_wie.py#L113)
- [TestFreeze.test_added_file_detected](../evaluation/witness-section19/research-archive/tests/test_wie.py#L119)
- [TestFreeze.test_refreeze_refused](../evaluation/witness-section19/research-archive/tests/test_wie.py#L125)
- [TestJudgesAndScore.test_unrun_i0_has_no_verdict_file_or_metrics_even_with_opt_in](../evaluation/witness-section19/research-archive/tests/test_wie.py#L139)
- [TestJudgesAndScore.test_archived_i0_can_only_be_regenerated_with_opt_in](../evaluation/witness-section19/research-archive/tests/test_wie.py#L144)
- [TestJudgesAndScore.test_i1_catches_exactly_the_same_frame_contradictions](../evaluation/witness-section19/research-archive/tests/test_wie.py#L151)
- [TestJudgesAndScore.test_i4_catches_state_errors_but_not_interpretation](../evaluation/witness-section19/research-archive/tests/test_wie.py#L160)
- [TestJudgesAndScore.test_i1_never_opens_workspace_and_i0_reads_only_self_assessment](../evaluation/witness-section19/research-archive/tests/test_wie.py#L167)
- [TestJudgesAndScore.test_judges_do_not_read_sealed](../evaluation/witness-section19/research-archive/tests/test_wie.py#L180)
- [TestImport.test_import_roundtrip_and_validation](../evaluation/witness-section19/research-archive/tests/test_wie.py#L189)
- [TestImport.test_import_rejects_unknown_ids_and_bad_verdicts](../evaluation/witness-section19/research-archive/tests/test_wie.py#L200)
- [TestImport.test_missing_requires_flag](../evaluation/witness-section19/research-archive/tests/test_wie.py#L210)
- [TestStats.test_wilson](../evaluation/witness-section19/research-archive/tests/test_wie.py#L222)
- [TestStats.test_mcnemar](../evaluation/witness-section19/research-archive/tests/test_wie.py#L228)

**[tests/test_blind_handoff.py](../tests/test_blind_handoff.py)**

- [BlindHandoffTests.test_target_packet_excludes_oracle_other_arm_and_hypothesis](../tests/test_blind_handoff.py#L13)
- [BlindHandoffTests.test_matched_arms_share_source_bytes](../tests/test_blind_handoff.py#L19)
- [BlindHandoffTests.test_future_source_is_unavailable_before_its_stage](../tests/test_blind_handoff.py#L25)
- [BlindHandoffTests.test_fault_injections_detect_smoothing_and_transfer_errors](../tests/test_blind_handoff.py#L30)
- [BlindHandoffTests.test_fabricated_read_cannot_pass](../tests/test_blind_handoff.py#L36)
- [BlindHandoffTests.test_export_contains_current_evidence_but_no_private_key](../tests/test_blind_handoff.py#L42)

**[tests/test_cad_reference.py](../tests/test_cad_reference.py)**

- [TestMapIsNotAuthority.test_stale_canonical_map_does_not_override_new_source](../tests/test_cad_reference.py#L32)
- [TestMapIsNotAuthority.test_map_only_never_becomes_cited_fact](../tests/test_cad_reference.py#L41)
- [TestMapIsNotAuthority.test_maximum_map_weight_is_not_more_evidence](../tests/test_cad_reference.py#L47)
- [TestMapIsNotAuthority.test_draft_not_current_authority](../tests/test_cad_reference.py#L53)
- [TestMapIsNotAuthority.test_blocked_source_cannot_support_claim](../tests/test_cad_reference.py#L58)
- [TestMapIsNotAuthority.test_orientation_carries_warning_and_current_status](../tests/test_cad_reference.py#L63)
- [TestMapIsNotAuthority.test_authorized_wrong_source_is_not_certified_truth](../tests/test_cad_reference.py#L71)
- [TestMapIsNotAuthority.test_no_claim_from_title_or_partial_literal_overlap](../tests/test_cad_reference.py#L79)
- [TestSourceConflictAndCorrection.test_two_intact_conflicting_sources_force_conflict](../tests/test_cad_reference.py#L86)
- [TestSourceConflictAndCorrection.test_unsupported_question_does_not_guess](../tests/test_cad_reference.py#L93)
- [TestSourceConflictAndCorrection.test_proposed_without_promotion_is_not_fact](../tests/test_cad_reference.py#L97)
- [TestSourceConflictAndCorrection.test_partial_correction_changes_one_field_only](../tests/test_cad_reference.py#L102)
- [TestSourceConflictAndCorrection.test_old_evidence_stops_after_successor_promotion](../tests/test_cad_reference.py#L113)
- [TestSourceConflictAndCorrection.test_stale_proposed_claim_cannot_be_promoted](../tests/test_cad_reference.py#L119)
- [TestSourceConflictAndCorrection.test_invalid_double_correction_refused](../tests/test_cad_reference.py#L125)
- [TestSourceConflictAndCorrection.test_wrong_subject_cannot_be_corrected](../tests/test_cad_reference.py#L132)
- [TestSourceConflictAndCorrection.test_reused_source_id_is_rejected](../tests/test_cad_reference.py#L138)
- [TestSourceConflictAndCorrection.test_successor_missing_old_source_rejected](../tests/test_cad_reference.py#L142)
- [TestProvenanceAndToEPressure.test_similarity_bridge_is_only_a_candidate](../tests/test_cad_reference.py#L148)
- [TestProvenanceAndToEPressure.test_repeated_map_as_proof_is_unsupported](../tests/test_cad_reference.py#L156)
- [TestProvenanceAndToEPressure.test_repeated_claim_mentions_do_not_create_other_fields](../tests/test_cad_reference.py#L161)
- [TestProvenanceAndToEPressure.test_authoritative_map_cannot_grant_itself_permissions](../tests/test_cad_reference.py#L166)
- [TestProvenanceAndToEPressure.test_copied_source_counts_are_not_independent_truth](../tests/test_cad_reference.py#L170)
- [TestProvenanceAndToEPressure.test_handle_collision_requires_namespace](../tests/test_cad_reference.py#L178)
- [TestProvenanceAndToEPressure.test_duplicate_handle_in_one_namespace_blocked](../tests/test_cad_reference.py#L184)
- [TestAuthorityContinuityAndReceipts.test_ungranted_worker_may_not_create_source](../tests/test_cad_reference.py#L190)
- [TestAuthorityContinuityAndReceipts.test_grant_is_narrow_and_revocable](../tests/test_cad_reference.py#L193)
- [TestAuthorityContinuityAndReceipts.test_worker_cannot_promote_fact](../tests/test_cad_reference.py#L199)
- [TestAuthorityContinuityAndReceipts.test_private_source_not_visible_to_unauthorized_guest](../tests/test_cad_reference.py#L205)
- [TestAuthorityContinuityAndReceipts.test_private_grant_revoke_rehides](../tests/test_cad_reference.py#L211)
- [TestAuthorityContinuityAndReceipts.test_message_stored_is_not_read_or_ack](../tests/test_cad_reference.py#L219)
- [TestAuthorityContinuityAndReceipts.test_sender_cannot_ack_for_recipient](../tests/test_cad_reference.py#L230)
- [TestAuthorityContinuityAndReceipts.test_ack_without_read_refused](../tests/test_cad_reference.py#L234)
- [TestAuthorityContinuityAndReceipts.test_restart_persists_source_and_revocation](../tests/test_cad_reference.py#L239)
- [TestAuthorityContinuityAndReceipts.test_event_tampering_detected_on_query](../tests/test_cad_reference.py#L249)
- [TestAuthorityContinuityAndReceipts.test_unauthorized_attempt_does_not_append_event](../tests/test_cad_reference.py#L254)
- [TestAuthorityContinuityAndReceipts.test_atomic_invalid_correction_does_not_append](../tests/test_cad_reference.py#L259)
- [TestAuthorityContinuityAndReceipts.test_actor_string_is_not_identity_authentication](../tests/test_cad_reference.py#L265)

**[tests/test_comparison_scope.py](../tests/test_comparison_scope.py)**

- [TestComparisonScope.test_instruction_and_native_counts_remain_separate](../tests/test_comparison_scope.py#L17)
- [TestComparisonScope.test_attribution_and_unrun_claims_are_preserved](../tests/test_comparison_scope.py#L34)
- [TestComparisonScope.test_public_driver_replay_distinguishes_question_labels_from_engine_results](../tests/test_comparison_scope.py#L51)

**[tests/test_critical_bench.py](../tests/test_critical_bench.py)**

- [CriticalBenchTests.test_reproducible_dimensions_and_unanimous_refusal_control](../tests/test_critical_bench.py#L19)
- [CriticalBenchTests.test_false_promotions_receipts_relations_and_duplicates_are_detected](../tests/test_critical_bench.py#L31)
- [CriticalBenchTests.test_fabricated_quote_and_missing_answers_fail](../tests/test_critical_bench.py#L42)
- [CriticalBenchTests.test_packets_match_evidence_hide_key_and_commit_before_scoring](../tests/test_critical_bench.py#L51)
- [CriticalBenchTests.test_retained_real_agent_records_replay](../tests/test_critical_bench.py#L69)
- [CriticalBenchTests.test_retained_critical_benchmark_and_known_score_limitations_replay](../tests/test_critical_bench.py#L74)
- [CriticalBenchTests.test_malformed_citation_is_a_failure_not_an_evaluator_crash](../tests/test_critical_bench.py#L81)

**[tests/test_discovery_bench.py](../tests/test_discovery_bench.py)**

- [DiscoveryTests.test_published_observations_replay_including_literal_action_failure](../tests/test_discovery_bench.py#L11)
- [DiscoveryTests.test_unknown_error_not_announced_and_sources_match_across_treatments](../tests/test_discovery_bench.py#L18)
- [DiscoveryTests.test_approved_error_is_persistently_wrong_without_evidential_override](../tests/test_discovery_bench.py#L29)

**[tests/test_human_export_bench.py](../tests/test_human_export_bench.py)**

- [HumanExportTests.test_observed_export_responses_replay_with_actions_preserved](../tests/test_human_export_bench.py#L9)
- [HumanExportTests.test_same_single_project_export_and_no_hidden_error_disclosure](../tests/test_human_export_bench.py#L16)
- [HumanExportTests.test_invented_independent_support_and_lineage_are_detected](../tests/test_human_export_bench.py#L25)

**[tests/test_independent_audit.py](../tests/test_independent_audit.py)**

- [IndependentAuditControls.test_refusal_label_does_not_certify_false_answer](../tests/test_independent_audit.py#L11)
- [IndependentAuditControls.test_handoff_missing_failure_is_detected](../tests/test_independent_audit.py#L17)
- [IndependentAuditControls.test_no_semantic_pass_from_matching_fields](../tests/test_independent_audit.py#L24)
- [IndependentAuditControls.test_invented_citation_fails](../tests/test_independent_audit.py#L29)
- [IndependentAuditControls.test_uncertainty_after_information_loss_is_not_hallucination](../tests/test_independent_audit.py#L33)
- [IndependentAuditControls.test_confident_wrong_conclusion_surviving_compression_is_identified](../tests/test_independent_audit.py#L39)
- [IndependentAuditControls.test_graph_scale_is_actual_input_not_a_thousand_word_claim](../tests/test_independent_audit.py#L44)
- [IndependentAuditControls.test_requests_have_no_hidden_oracle_or_prior_provider_session](../tests/test_independent_audit.py#L49)
- [IndependentAuditControls.test_verbatim_treatment_has_identifiable_published_boundaries](../tests/test_independent_audit.py#L54)

**[tests/test_kill_harness.py](../tests/test_kill_harness.py)**

- [TestFixtureAndContract.test_case_coverage_and_unique_ids](../tests/test_kill_harness.py#L22)
- [TestFixtureAndContract.test_anchors_and_source_hashes](../tests/test_kill_harness.py#L25)
- [TestFixtureAndContract.test_oracle_is_never_transmitted_to_target](../tests/test_kill_harness.py#L29)
- [TestFixtureAndContract.test_no_adapter_is_not_run](../tests/test_kill_harness.py#L34)
- [TestFixtureAndContract.test_stale_map_current_original_passes_contract](../tests/test_kill_harness.py#L38)
- [TestFixtureAndContract.test_false_map_value_fails](../tests/test_kill_harness.py#L40)
- [TestFixtureAndContract.test_map_citation_not_primary](../tests/test_kill_harness.py#L43)
- [TestFixtureAndContract.test_invented_source_quote_fails](../tests/test_kill_harness.py#L48)
- [TestFixtureAndContract.test_approved_false_claim_fails](../tests/test_kill_harness.py#L51)
- [TestFixtureAndContract.test_proven_influence_from_similarity_fails](../tests/test_kill_harness.py#L54)
- [TestFixtureAndContract.test_relational_saturation_at_three_scales_has_gates](../tests/test_kill_harness.py#L57)
- [TestFixtureAndContract.test_private_token_exposure_fails](../tests/test_kill_harness.py#L61)
- [TestFixtureAndContract.test_returning_restricted_citation_fails](../tests/test_kill_harness.py#L64)
- [TestFixtureAndContract.test_kill_gate_self_attestation_is_not_evidence](../tests/test_kill_harness.py#L67)
- [TestFixtureAndContract.test_independent_readback_detects_invalid_effect](../tests/test_kill_harness.py#L72)
- [TestFixtureAndContract.test_pruning_requires_zero_active_false_links](../tests/test_kill_harness.py#L79)
- [TestFixtureAndContract.test_independent_readback_requires_snapshot_pin](../tests/test_kill_harness.py#L83)
- [TestFixtureAndContract.test_modified_fixture_fails_closed](../tests/test_kill_harness.py#L86)

**[tests/test_native_evidence.py](../tests/test_native_evidence.py)**

- [NativeEvidenceTests.test_unmodified_full_native_suite_and_environment_failure_are_both_retained](../tests/test_native_evidence.py#L7)
- [NativeEvidenceTests.test_component_checks_preserve_exact_counts](../tests/test_native_evidence.py#L15)
- [NativeEvidenceTests.test_paired_current_guards_and_historical_gaps_are_not_erased](../tests/test_native_evidence.py#L20)

**[tests/test_oocc_correction.py](../tests/test_oocc_correction.py)**

- [CorrectionControls.test_oracle_controls_are_explicitly_not_model_results](../tests/test_oocc_correction.py#L9)
- [CorrectionControls.test_oracle_not_transmitted](../tests/test_oocc_correction.py#L12)
- [CorrectionControls.test_poisoned_state_is_not_repaired_by_harness](../tests/test_oocc_correction.py#L19)
- [CorrectionControls.test_bad_response_is_preserved_as_failure_not_clean_refusal](../tests/test_oocc_correction.py#L29)

**[tests/test_paired.py](../tests/test_paired.py)**

- [PairedHarnessTests.test_no_duplicate_cases](../tests/test_paired.py#L15)
- [PairedHarnessTests.test_references_pin_mplpb](../tests/test_paired.py#L18)
- [PairedHarnessTests.test_cad_and_baseline_see_identical_evidence](../tests/test_paired.py#L21)
- [PairedHarnessTests.test_correct_exact_answer_passes](../tests/test_paired.py#L26)
- [PairedHarnessTests.test_absent_citation_fails](../tests/test_paired.py#L30)
- [PairedHarnessTests.test_fabricated_citation_fails](../tests/test_paired.py#L34)
- [PairedHarnessTests.test_false_continuation_fails](../tests/test_paired.py#L38)
- [PairedHarnessTests.test_unwarranted_causation_fails](../tests/test_paired.py#L42)
- [PairedHarnessTests.test_refusal_passes_only_matching_oracle](../tests/test_paired.py#L46)
- [PairedHarnessTests.test_unsupported_arms_not_run](../tests/test_paired.py#L50)
- [PairedHarnessTests.test_no_native_as_theory_of_everything_proxy](../tests/test_paired.py#L56)
- [PairedHarnessTests.test_missing_native_source_marks_not_run](../tests/test_paired.py#L61)
- [PairedHarnessTests.test_unknown_manifest_schema_rejected](../tests/test_paired.py#L66)

**[tests/test_propagation_bench.py](../tests/test_propagation_bench.py)**

- [PropagationTests.test_preserved_actual_chains_replay_without_truth_detection_claim](../tests/test_propagation_bench.py#L8)
- [PropagationTests.test_only_original_access_changes_and_derivative_roots_never_multiply](../tests/test_propagation_bench.py#L15)
- [PropagationTests.test_harness_detects_authority_inflation_without_repairing_submission](../tests/test_propagation_bench.py#L23)

**[tests/test_public_claims.py](../tests/test_public_claims.py)**

- [PublicClaimTests.test_number_comparison_replays_and_retains_contrary_cases](../tests/test_public_claims.py#L10)
- [PublicClaimTests.test_dictionary_cost_includes_first_definition](../tests/test_public_claims.py#L20)
- [PublicClaimTests.test_reference_program_is_explicitly_ours](../tests/test_public_claims.py#L26)
- [PublicClaimTests.test_native_and_prompt_comparisons_are_never_pooled](../tests/test_public_claims.py#L33)
- [PublicClaimTests.test_packet_task_identity_and_missing_responses_stay_not_run](../tests/test_public_claims.py#L44)
- [PublicClaimTests.test_quotes_cannot_substitute_for_correct_values_or_source_binding](../tests/test_public_claims.py#L54)
- [PublicClaimTests.test_unrequested_claims_do_not_receive_a_perfect_contract_score](../tests/test_public_claims.py#L73)

**[tests/test_runner_subprocess.py](../tests/test_runner_subprocess.py)**

- [TestSubprocessBoundary.test_readonly_contract_mock_pass_not_native](../tests/test_runner_subprocess.py#L15)
- [TestSubprocessBoundary.test_fake_i_stopped_not_accepted_without_readback](../tests/test_runner_subprocess.py#L21)
- [TestSubprocessBoundary.test_observed_prohibited_publication_fails](../tests/test_runner_subprocess.py#L26)
- [TestSubprocessBoundary.test_invalid_json_is_adapter_error](../tests/test_runner_subprocess.py#L33)

**[tests/test_score_scaling.py](../tests/test_score_scaling.py)**

- [TestScalingScorer.test_negative_results_are_retained](../tests/test_score_scaling.py#L20)
- [TestScalingScorer.test_requires_preoutcome_registration](../tests/test_score_scaling.py#L26)
- [TestScalingScorer.test_requires_equal_access](../tests/test_score_scaling.py#L29)
- [TestScalingScorer.test_requires_blinded_reviews](../tests/test_score_scaling.py#L32)
- [TestScalingScorer.test_rejects_incomplete_scales](../tests/test_score_scaling.py#L35)
- [TestScalingScorer.test_rejects_mismatched_source_corpus](../tests/test_score_scaling.py#L38)
- [TestScalingScorer.test_rejects_bool_counts](../tests/test_score_scaling.py#L41)
- [TestScalingScorer.test_rejects_duplicate_arm](../tests/test_score_scaling.py#L44)
- [TestScalingScorer.test_rejects_false_links_exceeding_judged](../tests/test_score_scaling.py#L47)
- [TestScalingScorer.test_rejects_refuted_links_beyond_total](../tests/test_score_scaling.py#L50)

**[tests/test_sorter_random_batches.py](../tests/test_sorter_random_batches.py)**

- [SorterRandomBatchTests.test_seed_recreates_the_batch_and_key](../tests/test_sorter_random_batches.py#L10)
- [SorterRandomBatchTests.test_five_sets_and_four_distinct_cases_per_user](../tests/test_sorter_random_batches.py#L19)

**[tests/test_test_index.py](../tests/test_test_index.py)**

- [TestArchiveIndex.test_indexes_new_tests_and_evidence_without_treating_them_as_executions](../tests/test_test_index.py#L14)

**[tests/test_witness_live.py](../tests/test_witness_live.py)**

- [WitnessLiveHarness.test_writer_and_observer_use_real_slot_and_policy](../tests/test_witness_live.py#L21)
- [WitnessLiveHarness.test_missing_model_has_no_fabricated_scores](../tests/test_witness_live.py#L39)
- [WitnessLiveHarness.test_seeded_case_packet_is_repeatable](../tests/test_witness_live.py#L53)
- [WitnessLiveHarness.test_outside_judge_accepts_verified_outcomes](../tests/test_witness_live.py#L96)
- [WitnessLiveHarness.test_outside_judge_checks_claim_and_permission_against_effect](../tests/test_witness_live.py#L108)
- [WitnessLiveHarness.test_outside_judge_blocks_when_retained_bytes_changed](../tests/test_witness_live.py#L122)

**[tests/test_witness_separation.py](../tests/test_witness_separation.py)**

- [WitnessSeparationTests.test_greater_rejection_does_not_imply_discrimination](../tests/test_witness_separation.py#L27)
- [WitnessSeparationTests.test_gain_exceeding_false_alarm_budget_still_fails](../tests/test_witness_separation.py#L36)
- [WitnessSeparationTests.test_evidence_improvement_cannot_be_credited_to_separation](../tests/test_witness_separation.py#L43)
- [WitnessSeparationTests.test_abstention_can_raise_j_while_reducing_correct_decisions](../tests/test_witness_separation.py#L51)
- [WitnessSeparationTests.test_a_gain_with_state_does_not_make_the_gradient_monotonic](../tests/test_witness_separation.py#L60)
- [WitnessSeparationTests.test_genuine_monotonic_detection_gain_is_recognized](../tests/test_witness_separation.py#L69)
- [WitnessSeparationTests.test_missing_cases_are_not_silently_dropped_or_counted_as_abstentions](../tests/test_witness_separation.py#L78)
- [WitnessSeparationTests.test_missing_ground_truth_class_is_inconclusive](../tests/test_witness_separation.py#L87)

</details>

## Experiment and evidence collections

The JSON entry point lists suites and collections. The JSONL inventory includes every scoped
file, extracted case IDs and statuses, source line numbers, and archive member names.
Read the linked evidence for results and limitations. For example, search only Witness files with
`jq -c 'select(.collection == "evaluation/witness-section19")' research/test-inventory.jsonl`.

| Collection | Files | Case or status files | Entry points |
| --- | ---: | ---: | --- |
| [.](../.) | 5 | 0 | [README.md](../README.md) |
| [.github/workflows](../.github/workflows) | 10 | 0 |  |
| [blind](../blind) | 9 | 0 | [START.md](../blind/START.md) |
| [comparative-tests/dispatch-enforcement](../comparative-tests/dispatch-enforcement) | 10 | 2 | [README.md](../comparative-tests/dispatch-enforcement/README.md) · [results.json](../comparative-tests/dispatch-enforcement/results.json) |
| [comparative-tests/executable-gates](../comparative-tests/executable-gates) | 12 | 0 | [README.md](../comparative-tests/executable-gates/README.md) · [REPRODUCTION.md](../comparative-tests/executable-gates/REPRODUCTION.md) · [probes/results.json](../comparative-tests/executable-gates/probes/results.json) |
| [docs](../docs) | 19 | 0 |  |
| [docs/paper](../docs/paper) | 18 | 1 |  |
| [docs/papers](../docs/papers) | 45 | 4 | [README.md](../docs/papers/README.md) · [archive/README.md](../docs/papers/archive/README.md) |
| [evaluation](../evaluation) | 10 | 6 | [findings-index.json](../evaluation/findings-index.json) |
| [evaluation/agent-pilot-1](../evaluation/agent-pilot-1) | 3 | 1 | [summary.json](../evaluation/agent-pilot-1/summary.json) |
| [evaluation/critical-bench-1](../evaluation/critical-bench-1) | 20 | 4 | [summary.json](../evaluation/critical-bench-1/summary.json) |
| [evaluation/discovery-1](../evaluation/discovery-1) | 4 | 1 | [summary.json](../evaluation/discovery-1/summary.json) |
| [evaluation/human-export-1](../evaluation/human-export-1) | 3 | 0 | [summary.json](../evaluation/human-export-1/summary.json) |
| [evaluation/mplpb-native](../evaluation/mplpb-native) | 148 | 48 | [component-check/summary.json](../evaluation/mplpb-native/component-check/summary.json) · [final-seven-case-pairs/summary.json](../evaluation/mplpb-native/final-seven-case-pairs/summary.json) · [initial-five-case-pairs/summary.json](../evaluation/mplpb-native/initial-five-case-pairs/summary.json) · [network-enabled/summary.json](../evaluation/mplpb-native/network-enabled/summary.json) · 1 more in JSON |
| [evaluation/mplpb-updates](../evaluation/mplpb-updates) | 575 | 189 | [3df2c6e22f0ef454f3ee67b88d43402a42f63443/RESULTS.md](../evaluation/mplpb-updates/3df2c6e22f0ef454f3ee67b88d43402a42f63443/RESULTS.md) · [3df2c6e22f0ef454f3ee67b88d43402a42f63443/summary.json](../evaluation/mplpb-updates/3df2c6e22f0ef454f3ee67b88d43402a42f63443/summary.json) · [bbf6690d69b32d16969cc10e5ce9d380427ead40/RESULTS.md](../evaluation/mplpb-updates/bbf6690d69b32d16969cc10e5ce9d380427ead40/RESULTS.md) · [ccbb5804eb47f78c2338d57c142ad087b47be710/RESULTS.md](../evaluation/mplpb-updates/ccbb5804eb47f78c2338d57c142ad087b47be710/RESULTS.md) · 25 more in JSON |
| [evaluation/propagation-1](../evaluation/propagation-1) | 3 | 0 | [summary.json](../evaluation/propagation-1/summary.json) |
| [evaluation/public-claims](../evaluation/public-claims) | 131 | 24 | [2026-11-20/RESULTS.md](../evaluation/public-claims/2026-11-20/RESULTS.md) · [2026-11-20/observed-initial/summary.json](../evaluation/public-claims/2026-11-20/observed-initial/summary.json) · [2026-11-20/observed/summary.json](../evaluation/public-claims/2026-11-20/observed/summary.json) |
| [evaluation/public-papers](../evaluation/public-papers) | 34 | 1 | [RESULTS.md](../evaluation/public-papers/RESULTS.md) |
| [evaluation/witness-section19](../evaluation/witness-section19) | 101 | 27 | [RESULTS.md](../evaluation/witness-section19/RESULTS.md) · [live/README.md](../evaluation/witness-section19/live/README.md) · [live/REPORT.md](../evaluation/witness-section19/live/REPORT.md) · [research-archive/README.md](../evaluation/witness-section19/research-archive/README.md) · 2 more in JSON |
| [fixtures](../fixtures) | 5 | 3 |  |
| [oocc_lab](../oocc_lab) | 1 | 0 |  |
| [research](../research) | 18 | 3 |  |
| [research_lab](../research_lab) | 21 | 0 |  |
| [side_by_side](../side_by_side) | 7 | 1 | [README.md](../side_by_side/README.md) |
| [tests](../tests) | 19 | 0 |  |
| [tools](../tools) | 5 | 0 |  |

## Runnable scripts and workflow entry points

- [.github/workflows/bounded-documentary-acceptance.yml](../.github/workflows/bounded-documentary-acceptance.yml)
- [.github/workflows/codex-handoff.yml](../.github/workflows/codex-handoff.yml)
- [.github/workflows/current-mplpb-acceptance.yml](../.github/workflows/current-mplpb-acceptance.yml)
- [.github/workflows/mplpb-native-comparison.yml](../.github/workflows/mplpb-native-comparison.yml)
- [.github/workflows/oocc-correction.yml](../.github/workflows/oocc-correction.yml)
- [.github/workflows/paired-cad-live.yml](../.github/workflows/paired-cad-live.yml)
- [.github/workflows/paired-mplpb.yml](../.github/workflows/paired-mplpb.yml)
- [.github/workflows/public-claims.yml](../.github/workflows/public-claims.yml)
- [.github/workflows/test-index.yml](../.github/workflows/test-index.yml)
- [.github/workflows/tests.yml](../.github/workflows/tests.yml)
- [comparative-tests/dispatch-enforcement/run_controls.py](../comparative-tests/dispatch-enforcement/run_controls.py)
- [comparative-tests/executable-gates/probes/git_probe.sh](../comparative-tests/executable-gates/probes/git_probe.sh)
- [comparative-tests/executable-gates/verify.py](../comparative-tests/executable-gates/verify.py)
- [evaluation/mplpb-updates/3df2c6e22f0ef454f3ee67b88d43402a42f63443/retry_component.py](../evaluation/mplpb-updates/3df2c6e22f0ef454f3ee67b88d43402a42f63443/retry_component.py)
- [evaluation/mplpb-updates/3df2c6e22f0ef454f3ee67b88d43402a42f63443/run_checks.py](../evaluation/mplpb-updates/3df2c6e22f0ef454f3ee67b88d43402a42f63443/run_checks.py)
- [evaluation/mplpb-updates/3df2c6e22f0ef454f3ee67b88d43402a42f63443/run_components.py](../evaluation/mplpb-updates/3df2c6e22f0ef454f3ee67b88d43402a42f63443/run_components.py)
- [evaluation/mplpb-updates/3df2c6e22f0ef454f3ee67b88d43402a42f63443/run_extras.py](../evaluation/mplpb-updates/3df2c6e22f0ef454f3ee67b88d43402a42f63443/run_extras.py)
- [evaluation/mplpb-updates/ccbb5804eb47f78c2338d57c142ad087b47be710/run_checks.py](../evaluation/mplpb-updates/ccbb5804eb47f78c2338d57c142ad087b47be710/run_checks.py)
- [evaluation/mplpb-updates/ccbb5804eb47f78c2338d57c142ad087b47be710/run_components.py](../evaluation/mplpb-updates/ccbb5804eb47f78c2338d57c142ad087b47be710/run_components.py)
- [evaluation/mplpb-updates/ccbb5804eb47f78c2338d57c142ad087b47be710/run_extras.py](../evaluation/mplpb-updates/ccbb5804eb47f78c2338d57c142ad087b47be710/run_extras.py)
- [evaluation/mplpb-updates/ccbb5804eb47f78c2338d57c142ad087b47be710/run_frozen_papers.py](../evaluation/mplpb-updates/ccbb5804eb47f78c2338d57c142ad087b47be710/run_frozen_papers.py)
- [evaluation/mplpb-updates/ccbb5804eb47f78c2338d57c142ad087b47be710/run_predecessors.py](../evaluation/mplpb-updates/ccbb5804eb47f78c2338d57c142ad087b47be710/run_predecessors.py)
- [evaluation/public-claims/2026-11-20/producer-initial.py](../evaluation/public-claims/2026-11-20/producer-initial.py)
- [evaluation/public-claims/2026-11-20/producer.py](../evaluation/public-claims/2026-11-20/producer.py)
- [evaluation/public-papers/run.py](../evaluation/public-papers/run.py)
- [evaluation/witness-section19/live/check_tools.py](../evaluation/witness-section19/live/check_tools.py)
- [evaluation/witness-section19/live/effects.py](../evaluation/witness-section19/live/effects.py)
- [evaluation/witness-section19/live/handoff.py](../evaluation/witness-section19/live/handoff.py)
- [evaluation/witness-section19/live/judge.py](../evaluation/witness-section19/live/judge.py)
- [evaluation/witness-section19/live/outside_judge.py](../evaluation/witness-section19/live/outside_judge.py)
- [evaluation/witness-section19/live/run.py](../evaluation/witness-section19/live/run.py)
- [evaluation/witness-section19/live/score.py](../evaluation/witness-section19/live/score.py)
- [evaluation/witness-section19/live/separation.py](../evaluation/witness-section19/live/separation.py)
- [evaluation/witness-section19/research-archive/wie/__main__.py](../evaluation/witness-section19/research-archive/wie/__main__.py)
- [make_cases.py](../make_cases.py)
- [research_lab/agent_entry.py](../research_lab/agent_entry.py)
- [research_lab/agent_replay.py](../research_lab/agent_replay.py)
- [research_lab/archive_monitor.py](../research_lab/archive_monitor.py)
- [research_lab/blind_handoff.py](../research_lab/blind_handoff.py)
- [research_lab/critical_bench.py](../research_lab/critical_bench.py)
- [research_lab/discovery_bench.py](../research_lab/discovery_bench.py)
- [research_lab/freeze.py](../research_lab/freeze.py)
- [research_lab/human_export_bench.py](../research_lab/human_export_bench.py)
- [research_lab/live.py](../research_lab/live.py)
- [research_lab/mplpb_native_suite.py](../research_lab/mplpb_native_suite.py)
- [research_lab/mplpb_parts_suite.py](../research_lab/mplpb_parts_suite.py)
- [research_lab/mplpb_seam_probe.py](../research_lab/mplpb_seam_probe.py)
- [research_lab/native_evidence.py](../research_lab/native_evidence.py)
- [research_lab/oocc_adversarial.py](../research_lab/oocc_adversarial.py)
- [research_lab/propagation_bench.py](../research_lab/propagation_bench.py)
- [research_lab/public_claims.py](../research_lab/public_claims.py)
- [research_lab/sorter_mixed_users.py](../research_lab/sorter_mixed_users.py)
- [research_lab/sorter_random_batches.py](../research_lab/sorter_random_batches.py)
- [research_lab/witness_section19.py](../research_lab/witness_section19.py)
- [side_by_side/github_models_adapter.py](../side_by_side/github_models_adapter.py)
- [side_by_side/run.py](../side_by_side/run.py)
- [tools/build_critical_paper.py](../tools/build_critical_paper.py)
- [tools/build_test_index.py](../tools/build_test_index.py)
- [tools/kill_harness.py](../tools/kill_harness.py)
- [tools/score_scaling.py](../tools/score_scaling.py)
- [tools/verify_oocc_claim_roadmap.py](../tools/verify_oocc_claim_roadmap.py)

## Regenerate or verify

```sh
python -m tools.build_test_index
python -m tools.build_test_index --check
```

Stage new files before regenerating locally. GitHub Actions refreshes the index after
changes reach `main`. Generation is deterministic and does not execute the indexed tests.
