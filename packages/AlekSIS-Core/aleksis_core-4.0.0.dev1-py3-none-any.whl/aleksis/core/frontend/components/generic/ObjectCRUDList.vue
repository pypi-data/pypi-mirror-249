<script setup>
import CreateButton from "./buttons/CreateButton.vue";
import DialogObjectForm from "./dialogs/DialogObjectForm.vue";
</script>

<template>
  <v-card>
    <v-data-iterator
      :items="items"
      :items-per-page="itemsPerPage"
      :loading="$apollo.queries.items.loading"
      hide-default-footer
    >
      <template #loading>
        <slot name="loading">
          <v-skeleton-loader
            type="card-heading, list-item-avatar-two-line@3, actions"
          />
        </slot>
      </template>

      <template #no-data>
        <v-card-text>{{ $t(noItemsI18nKey) }}</v-card-text>
      </template>

      <template #header>
        <v-card-title>{{ title }}</v-card-title>
      </template>

      <template #default="props">
        <slot
          v-if="items.length"
          name="iteratorContent"
          :items="props.items"
          :editing-enabled="editingEnabled"
          :deletion-enabled="deletionEnabled"
          :handle-edit="handleEdit"
          :handle-delete="handleDelete"
        >
          <v-list>
            <template v-for="(item, index) in items">
              <v-list-item :key="item.id">
                <v-list-item-avatar>
                  <slot
                    name="listIteratorItemAvatar"
                    :item="item"
                    :index="index"
                  />
                </v-list-item-avatar>
                <v-list-item-content>
                  <slot
                    name="listIteratorItemContent"
                    :item="item"
                    :index="index"
                  >
                    <v-list-item-title>
                      {{ item.name }}
                    </v-list-item-title>
                  </slot>
                </v-list-item-content>
                <v-list-item-action>
                  <v-btn
                    v-if="editingEnabled && item.canEdit"
                    icon
                    @click="handleEdit(item)"
                  >
                    <v-icon>mdi-pencil-outline</v-icon>
                  </v-btn>
                  <v-btn
                    v-if="deletionEnabled && item.canDelete"
                    icon
                    @click="handleDelete(item)"
                  >
                    <v-icon>mdi-delete-outline</v-icon>
                  </v-btn>
                </v-list-item-action>
              </v-list-item>
              <v-divider
                v-if="index < items.length - 1"
                :key="index"
                inset
              ></v-divider>
            </template>
          </v-list>
        </slot>
      </template>

      <template #footer>
        <v-card-actions>
          <slot
            v-if="creatingEnabled || editingEnabled"
            name="createComponent"
            :attrs="{
              value: objectFormModel,
              defaultItem: defaultItem,
              editItem: editItem,
              gqlCreateMutation: gqlCreateMutation,
              gqlPatchMutation: gqlPatchMutation,
              isCreate: isCreate,
              fields: fields,
              getCreateData: getCreateData,
              createItemI18nKey: createItemI18nKey,
            }"
            :on="{
              input: (i) => (objectFormModel = i),
              cancel: () => (objectFormModel = false),
              save: handleCreateDone,
              error: handleError,
            }"
          >
            <dialog-object-form
              v-model="objectFormModel"
              :get-create-data="getCreateData"
              :get-patch-data="getPatchData"
              :default-item="defaultItem"
              :edit-item="editItem"
              :force-model-item-update="true"
              :gql-create-mutation="gqlCreateMutation"
              :gql-patch-mutation="gqlPatchMutation"
              :is-create="isCreate"
              :fields="fields"
              :create-item-i18n-key="createItemI18nKey"
              @cancel="objectFormModel = false"
              @save="handleCreateDone"
              @error="handleError"
            >
              <template #activator="{ props }" v-if="creatingEnabled">
                <create-button
                  @click="handleCreate"
                  :disabled="objectFormModel"
                />
              </template>

              <template
                v-for="field in fields"
                #[formFieldSlotName(field)]="{ item, isCreate, on, attrs }"
              >
                <slot
                  :name="formFieldSlotName(field)"
                  :attrs="attrs"
                  :on="on"
                  :item="item"
                  :is-create="isCreate"
                />
              </template>
            </dialog-object-form>
          </slot>
        </v-card-actions>
      </template>
    </v-data-iterator>
  </v-card>
</template>

<script>
export default {
  name: "ObjectCRUDList",
  props: {
    titleI18nKey: {
      type: String,
      required: false,
      default: "",
    },
    titleString: {
      type: String,
      required: false,
      default: "",
    },
    noItemsI18nKey: {
      type: String,
      required: true,
    },
    createItemI18nKey: {
      type: String,
      required: false,
      default: "actions.create",
    },
    fields: {
      type: Array,
      required: false,
      default: undefined,
    },
    defaultItem: {
      type: Object,
      required: false,
      default: undefined,
    },
    getGqlData: {
      type: Function,
      required: false,
      default: (data) => data.items,
    },
    gqlQuery: {
      type: Object,
      required: true,
    },
    gqlVariables: {
      type: Object,
      required: false,
      default: undefined,
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
    getCreateData: {
      type: Function,
      required: false,
      default: (item) => item,
    },
    getPatchData: {
      type: Function,
      required: false,
      default: (item) => {
        let { id, __typename, ...patchItem } = item;
        return patchItem;
      },
    },
    itemsPerPage: {
      type: Number,
      required: false,
      default: 5,
    },
  },
  components: {
    CreateButton,
  },
  data() {
    return {
      objectFormModel: false,
      editItem: undefined,
      isCreate: true,
    };
  },
  apollo: {
    items() {
      return {
        query: this.gqlQuery,
        variables() {
          if (this.gqlVariables) {
            return this.gqlVariables;
          }
          return {};
        },
        error: function (error) {
          this.handleError(error);
        },
        update(data) {
          return this.getGqlData(data);
        },
      };
    },
  },
  methods: {
    handleCreate() {
      this.editItem = undefined;
      this.isCreate = true;
      this.objectFormModel = true;
    },
    handleEdit(item) {
      if (!item || !this.editingEnabled) {
        return;
      }

      this.editItem = item;
      this.isCreate = false;
      this.objectFormModel = true;
    },
    handleDelete() {},
    handleCreateDone() {
      this.$apollo.queries.items.refetch();
    },
    handleError(error) {
      console.error(error);
      let snackbarText = "";
      if (error instanceof String) {
        // error is a translation key or simply a string
        snackbarText = this.$t(error);
      } else if (error instanceof Object && error.message) {
        snackbarText = error.message;
      } else {
        snackbarText = this.$t("graphql.snackbar_error_message");
      }
      this.$root.snackbarItems.push({
        id: crypto.randomUUID(),
        timeout: 5000,
        messageKey: snackbarText,
        color: "error",
      });
    },
    formFieldSlotName(headerEntry) {
      return headerEntry.value + ".field";
    },
  },
  computed: {
    creatingEnabled() {
      return this.gqlCreateMutation && this.fields && this.defaultItem;
    },
    editingEnabled() {
      return (
        this.gqlPatchMutation &&
        this.fields &&
        this.items &&
        this.items.some((i) => i.canEdit)
      );
    },
    deletionEnabled() {
      return (
        this.gqlDeleteMutation &&
        this.items &&
        this.items.some((i) => i.canDelete)
      );
    },
    title() {
      return this.titleI18nKey ? this.$t(this.titleI18nKey) : this.titleString;
    },
  },
};
</script>

<style scoped></style>
