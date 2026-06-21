export type InheritanceModal = 'buy' | 'info' | null;

export const stateInheritanceUi = $state({
	modal: null as InheritanceModal,
});
