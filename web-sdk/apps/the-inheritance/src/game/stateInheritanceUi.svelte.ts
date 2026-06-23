export type InheritanceModal = 'buy' | 'info' | 'legacyFeatureUnlocked' | null;

export const stateInheritanceUi = $state({
	modal: null as InheritanceModal,
});
