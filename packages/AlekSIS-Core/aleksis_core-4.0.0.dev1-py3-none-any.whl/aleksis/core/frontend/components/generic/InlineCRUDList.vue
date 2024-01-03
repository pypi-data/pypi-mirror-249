<template>
  <div>
    <delete-dialog
      v-if="deletionEnabled"
      :gql-mutation="gqlDeleteMutation"
      :gql-query="$apollo.queries.items"
      v-model="deletionDialog"
      :item="itemToDelete"
      @input="handleDeleteDone"
      :item-attribute="itemTitleAttribute"
    />

    <delete-multiple-dialog
      v-if="multipleDeletionEnabled"
      :gql-mutation="gqlDeleteMultipleMutation"
      :gql-query="$apollo.queries.items"
      :items="itemsToDelete"
      v-model="multipleDeletionDialog"
      @input="handleDeleteDone"
      :item-attribute="itemTitleAttribute"
    />

    <v-form v-model="valid">
      <v-data-table
        :headers="tableHeaders"
        :items="editableItems"
        :loading="$apollo.loading"
        :class="elevationClass"
        :items-per-page="15"
        :search="search"
        :sort-by.sync="sortBy"
        :sort-desc.sync="sortDesc"
        multi-sort
        @update:sort-by="handleSortChange"
        @update:sort-desc="handleSortChange"
        :show-select="generatedActions.length > 0"
        selectable-key="canDelete"
        @item-selected="handleItemSelected"
        @toggle-select-all="handleToggleAll"
        @current-items="checkSelectAll"
        :show-expand="showExpand"
      >
        <template #top>
          <v-toolbar flat class="height-fit child-height-fit">
            <v-row class="flex-wrap gap align-baseline pt-4">
              <v-toolbar-title class="d-flex flex-wrap w-100 gap">
                <filter-button
                  class="my-1 button-40"
                  :num-filters="numFilters"
                  v-if="filter"
                  @click="requestFilter"
                  @clear="clearFilters"
                />

                <filter-dialog
                  v-model="filterDialog"
                  :filters="filters"
                  @filters="handleFiltersChanged"
                >
                  <template #default="slotProps">
                    <slot
                      name="filters"
                      v-if="filter"
                      v-bind="slotProps"
                    ></slot>
                  </template>
                </filter-dialog>

                <div class="my-1">
                  <v-text-field
                    v-model="search"
                    type="search"
                    clearable
                    rounded
                    filled
                    hide-details
                    single-line
                    prepend-inner-icon="$search"
                    dense
                    outlined
                    :placeholder="$t('actions.search')"
                  />
                </div>

                <div
                  v-if="generatedActions.length > 0 && selectedItems.length > 0"
                  class="my-1"
                >
                  <v-autocomplete
                    auto-select-first
                    clearable
                    :items="generatedActions"
                    v-model="selectedAction"
                    return-object
                    :label="$t('actions.select_action')"
                    item-text="name"
                    outlined
                    dense
                    :hint="
                      $tc('selection.num_items_selected', selectedItems.length)
                    "
                    persistent-hint
                    append-outer-icon="$send"
                    @click:append-outer="handleAction"
                  >
                    <template #item="{ item, attrs, on }">
                      <v-list-item dense v-bind="attrs" v-on="on">
                        <v-list-item-icon v-if="item.icon">
                          <v-icon>{{ item.icon }}</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                          <v-list-item-title>{{ item.name }}</v-list-item-title>
                        </v-list-item-content>
                      </v-list-item>
                    </template>
                  </v-autocomplete>
                </div>
              </v-toolbar-title>

              <v-spacer
                class="flex-grow-0 flex-sm-grow-1 mx-n1 mx-sm-0"
              ></v-spacer>
              <slot
                v-if="!editMode && showCreate"
                name="createComponent"
                :attrs="{
                  value: createMode,
                  getCreateData: getCreateData,
                  defaultItem: defaultItem,
                  gqlQuery: gqlQuery,
                  gqlCreateMutation: gqlCreateMutation,
                  gqlPatchMutation: gqlPatchMutation,
                  isCreate: true,
                  fields: editableHeaders,
                  createItemI18nKey: createItemI18nKey,
                }"
                :on="{
                  input: (i) => (i ? requestCreate() : null),
                  cancel: cancelCreate,
                  save: handleCreateDone,
                  error: handleError,
                }"
                :create-mode="createMode"
                :form-field-slot-name="formFieldSlotName"
              >
                <dialog-object-form
                  v-model="createMode"
                  :get-create-data="getCreateData"
                  :default-item="defaultItem"
                  :gql-create-mutation="gqlCreateMutation"
                  :gql-patch-mutation="gqlPatchMutation"
                  :is-create="true"
                  :fields="editableHeaders"
                  :create-item-i18n-key="createItemI18nKey"
                  @cancel="cancelCreate"
                  @save="handleCreateDone"
                  @error="handleError"
                >
                  <template #activator="{ props }">
                    <create-button
                      color="secondary"
                      @click="requestCreate"
                      :disabled="createMode"
                    />
                  </template>

                  <template
                    v-for="header in editableHeaders"
                    #[formFieldSlotName(header)]="{ item, isCreate, on, attrs }"
                  >
                    <slot
                      :name="formFieldSlotName(header)"
                      :attrs="attrs"
                      :on="on"
                      :item="item"
                      :is-create="isCreate"
                    />
                  </template>
                </dialog-object-form>
              </slot>
              <edit-button
                v-if="!editMode && editingEnabled"
                @click="requestEdit"
                :disabled="createMode"
              />
              <cancel-button v-if="editMode" @click="cancelEdit" />
              <save-button
                v-if="editMode"
                @click="saveEdit"
                :loading="loading"
                :disabled="!valid"
              />
            </v-row>
          </v-toolbar>
        </template>

        <template
          v-for="(header, idx) in headers"
          #[tableItemSlotName(header)]="{ item }"
        >
          <v-scroll-x-transition mode="out-in" :key="idx">
            <span key="value" v-if="!editMode || header.disableEdit">
              <slot :name="header.value" :item="item">{{
                item[header.value]
              }}</slot>
            </span>
            <span key="field" v-else-if="editMode">
              <slot
                :name="header.value + '.field'"
                :item="item"
                :is-create="false"
                :attrs="buildAttrs(item[header.value])"
                :on="buildOn(dynamicSetter(item, header.value))"
              >
                <v-text-field
                  filled
                  dense
                  hide-details="auto"
                  v-model="item[header.value]"
                ></v-text-field>
              </slot>
            </span>
          </v-scroll-x-transition>
        </template>

        <!-- eslint-disable-next-line vue/valid-v-slot -->
        <template #item.actions="{ item }">
          <slot name="actions" :item="item" />
          <v-btn
            v-if="'canDelete' in item && item.canDelete"
            icon
            :title="$t(`actions.delete`)"
            color="error"
            @click="handleDeleteClick(item)"
          >
            <v-icon>$deleteContent</v-icon>
          </v-btn>
        </template>

        <template #expanded-item="{ headers, item }">
          <td :colspan="headers.length">
            <slot name="expanded-item" :item="item" />
          </td>
        </template>
      </v-data-table>
    </v-form>

    <closable-snackbar :color="snackbarState" v-model="snackbar">
      {{ snackbarText }}
    </closable-snackbar>
  </div>
</template>

<script>
import CreateButton from "./buttons/CreateButton.vue";
import EditButton from "./buttons/EditButton.vue";
import SaveButton from "./buttons/SaveButton.vue";
import CancelButton from "./buttons/CancelButton.vue";
import DeleteDialog from "./dialogs/DeleteDialog.vue";
import DeleteMultipleDialog from "./dialogs/DeleteMultipleDialog.vue";
import DialogObjectForm from "./dialogs/DialogObjectForm.vue";
import ClosableSnackbar from "./dialogs/ClosableSnackbar.vue";
import FilterButton from "./buttons/FilterButton.vue";
import FilterDialog from "./dialogs/FilterDialog.vue";

export default {
  name: "InlineCRUDList",
  components: {
    FilterDialog,
    FilterButton,
    ClosableSnackbar,
    DeleteDialog,
    DeleteMultipleDialog,
    DialogObjectForm,
    CancelButton,
    SaveButton,
    EditButton,
    CreateButton,
  },

  apollo: {
    items() {
      return {
        query: this.gqlQuery,
        variables() {
          return {
            ...this.additionalQueryArgs,
            orderBy: this.gqlOrderBy,
            filters: this.filterString,
          };
        },
        error: function (error) {
          this.handleError(error);
        },
        result: function (data) {
          this.editableItems = data.data
            ? this.getGqlData(JSON.parse(JSON.stringify(data.data.items)))
            : [];
        },
      };
    },
  },
  data() {
    return {
      editMode: false,
      createMode: false,
      loading: false,
      createModel: {},
      editableItems: [],
      snackbar: false,
      snackbarText: null,
      snackbarState: "success",
      valid: false,
      deletionDialog: false,
      multipleDeletionDialog: false,
      itemToDelete: null,
      itemsToDelete: [],
      search: "",
      filterDialog: false,
      filters: {},
      filterString: "{}",
      sortBy: [],
      sortDesc: [],
      gqlOrderBy: [],
      selectedAction: null,
      selectedItems: [],
      allSelected: false,
    };
  },
  computed: {
    tableHeaders() {
      return this.headers
        .concat(
          this.deletionEnabled
            ? [
                {
                  text: this.$t("actions.title"),
                  value: "actions",
                  sortable: false,
                  align: "right",
                },
              ]
            : [],
        )
        .filter((header) => this.hiddenColumns.indexOf(header.value) === -1);
    },
    editableHeaders() {
      return this.headers.filter((header) => !header.disableEdit);
    },
    elevationClass() {
      return this.elevated ? "elevation-2" : "";
    },
    editingEnabled() {
      return (
        this.gqlPatchMutation && this.items && this.items.some((i) => i.canEdit)
      );
    },
    deletionEnabled() {
      return (
        this.gqlDeleteMutation &&
        this.items &&
        this.items.some((i) => i.canDelete)
      );
    },
    multipleDeletionEnabled() {
      return (
        this.multipleDeletion &&
        this.gqlDeleteMultipleMutation &&
        this.items &&
        this.items.some((i) => i.canDelete)
      );
    },
    numFilters() {
      // This needs to use the json string, as vue reactivity doesn't work for objects with dynamic properties
      return Object.keys(JSON.parse(this.filterString)).length;
    },
    generatedActions() {
      if (!this.multipleDeletionEnabled) {
        return this.actions;
      }
      return [
        ...this.actions,
        {
          name: this.$t("actions.delete"),
          icon: "$deleteContent",
          handler: (items) => {
            this.itemsToDelete = items;
            this.multipleDeletionDialog = true;
          },
          clearSelection: true,
        },
      ];
    },
  },
  props: {
    i18nKey: {
      type: String,
      required: true,
    },
    createItemI18nKey: {
      type: String,
      required: false,
      default: "actions.create",
    },
    createSuccessMessageKey: {
      type: String,
      required: false,
      default: "status.object_create_success",
    },
    gqlQuery: {
      type: Object,
      required: true,
    },
    additionalQueryArgs: {
      type: Object,
      required: false,
      default: () => ({}),
    },
    gqlCreateMutation: {
      type: Object,
      required: false,
      default: undefined,
    },
    gqlPatchMutation: {
      type: Object,
      required: false,
      default: undefined,
    },
    gqlDeleteMutation: {
      type: Object,
      required: false,
      default: undefined,
    },
    gqlDeleteMultipleMutation: {
      type: Object,
      required: false,
      default: undefined,
    },
    headers: {
      type: Array,
      required: true,
    },
    itemTitleAttribute: {
      type: String,
      required: false,
      default: "name",
    },
    defaultItem: {
      type: Object,
      required: true,
    },
    showCreate: {
      type: Boolean,
      required: false,
      default: true,
    },
    elevated: {
      type: Boolean,
      required: false,
      default: true,
    },
    hiddenColumns: {
      type: Array,
      required: false,
      default: () => [],
    },
    getGqlData: {
      type: Function,
      required: false,
      default: (item) => item,
    },
    getPatchData: {
      type: Function,
      required: false,
      default: (items, headers) => {
        return items.map((item) => {
          let dto = {};
          headers.map((header) => (dto[header.value] = item[header.value]));
          return dto;
        });
      },
    },
    getCreateData: {
      type: Function,
      required: false,
      default: (item) => item,
    },
    filter: {
      type: Boolean,
      required: false,
      default: false,
    },
    actions: {
      type: Array,
      required: false,
      default: () => [],
    },
    multipleDeletion: {
      type: Boolean,
      required: false,
      default: true,
    },
    showExpand: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  methods: {
    requestCreate() {
      if (this.loading) return;

      this.createMode = true;
      this.editMode = false;
    },
    requestEdit() {
      if (this.loading) return;

      this.editMode = true;
      this.createMode = false;
    },
    saveEdit() {
      this.loading = true;

      if (!this.editableItems || !this.editingEnabled) return;

      this.$apollo
        .mutate({
          mutation: this.gqlPatchMutation,
          variables: {
            input: this.getPatchData(
              this.editableItems,
              this.headers.concat({ title: "id", value: "id" }),
            ),
          },
        })
        .then((data) => {
          this.items = data.data.batchMutation.items;
          this.editableItems = this.getGqlData(data.data.batchMutation.items);

          this.handleSuccess("status.saved");
        })
        .catch((error) => {
          this.handleError(error);
        })
        .finally(() => {
          this.loading = false;
          this.editMode = false;
        });
    },
    cancelEdit() {
      this.editMode = false;
      this.editableItems = this.getGqlData(
        JSON.parse(JSON.stringify(this.items)),
      );
    },
    saveCreate() {
      if (!this.gqlCreateMutation) return;

      this.loading = true;
      this.$apollo
        .mutate({
          mutation: this.gqlCreateMutation,
          variables: {
            input: this.createModel,
          },
        })
        .then((data) => {
          this.$apollo.queries.items.refetch();
          this.createModel = {};
        })
        .catch((error) => {
          this.handleError(error);
        })
        .finally(() => {
          this.loading = false;
          this.createMode = false;
        });
    },
    cancelCreate() {
      this.createMode = false;
      this.createModel = {};
    },
    tableItemSlotName(headerEntry) {
      return "item." + headerEntry.value;
    },
    formFieldSlotName(headerEntry) {
      return headerEntry.value + ".field";
    },
    dynamicSetter(item, fieldName) {
      return (value) => {
        this.$set(item, fieldName, value);
      };
    },
    handleError(error) {
      console.error(error);
      if (error instanceof String) {
        // error is a translation key or simply a string
        this.snackbarText = this.$t(error);
      } else if (error instanceof Object && error.message) {
        this.snackbarText = error.message;
      } else {
        this.snackbarText = this.$t("graphql.snackbar_error_message");
      }
      this.snackbarState = "error";
      this.snackbar = true;
    },
    handleSuccess(success) {
      this.snackbarText = this.$t(
        success || "graphql.snackbar_success_message",
      );

      this.snackbarState = "success";
      this.snackbar = true;
    },
    handleDeleteClick(item) {
      if (!item) {
        console.warn("Delete handler called without item parameter");
        return;
      }

      this.itemToDelete = item;
      this.deletionDialog = true;
    },
    handleDeleteDone() {
      this.itemToDelete = null;
      this.itemsToDelete = [];
    },
    handleCreateDone() {
      this.$apollo.queries.items.refetch();
      this.createMode = false;
    },
    requestFilter() {
      if (this.filter) {
        this.filterDialog = true;
      }
    },
    handleFiltersChanged(event) {
      this.filters = event;
      this.filterString = JSON.stringify(this.filters);
    },
    clearFilters() {
      this.handleFiltersChanged({});
    },
    buildAttrs(value) {
      return {
        dense: true,
        filled: true,
        hideDetails: "auto",
        value: value,
        inputValue: value,
      };
    },
    buildOn(setter) {
      return {
        input: setter,
        change: setter,
      };
    },
    snakeCase(string) {
      return string
        .replace(/\W+/g, " ")
        .split(/ |\B(?=[A-Z])/)
        .map((word) => word.toLowerCase())
        .join("_");
    },
    orderKey(value, desc) {
      const key =
        this.headers.find((header) => header.value === value).orderKey ||
        this.snakeCase(value);
      return (desc ? "-" : "") + key;
    },
    handleSortChange() {
      this.gqlOrderBy = this.sortBy.map((value, key) =>
        this.orderKey(value, this.sortDesc[key]),
      );
    },
    handleItemSelected({ item, value }) {
      if (value) {
        this.selectedItems.push(item);
      } else {
        const index = this.selectedItems.indexOf(item);
        if (index >= 0) {
          this.selectedItems.splice(index, 1);
        }
      }
    },
    handleToggleAll({ items, value }) {
      if (value) {
        // There is a bug in vuetify: items contains all elements, even those that aren't selectable
        this.selectedItems = items.filter((item) => item.canDelete || false);
      } else {
        this.selectedItems = [];
      }
      this.allSelected = value;
    },
    checkSelectAll(newItems) {
      if (this.allSelected) {
        this.handleToggleAll({
          items: newItems,
          value: true,
        });
      }
    },
    handleAction() {
      if (this.selectedAction) {
        this.selectedAction.handler(this.selectedItems);

        if (this.selectedAction.clearSelection) {
          this.selectedItems = [];
        }

        this.selectedAction = null;
      }
    },
  },
  mounted() {
    this.$setToolBarTitle(this.$t(`${this.i18nKey}.title_plural`), null);
  },
};
</script>

<style>
.gap {
  gap: 0.5rem;
}
.height-fit,
.child-height-fit > * {
  height: fit-content !important;
}

.button-40 {
  min-height: 40px;
}
</style>
