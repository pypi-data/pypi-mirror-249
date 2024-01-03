<script setup>
import InlineCRUDList from "../generic/InlineCRUDList.vue";
</script>

<template>
  <inline-c-r-u-d-list
    :headers="headers"
    :i18n-key="i18nKey"
    create-item-i18n-key="rooms.create_room"
    :gql-query="gqlQuery"
    :gql-create-mutation="gqlCreateMutation"
    :gql-patch-mutation="gqlPatchMutation"
    :gql-delete-mutation="gqlDeleteMutation"
    :gql-delete-multiple-mutation="gqlDeleteMultipleMutation"
    :default-item="defaultItem"
  >
    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #shortName.field="{ attrs, on, isCreate }">
      <div aria-required="true">
        <v-text-field
          v-bind="attrs"
          v-on="on"
          required
          :rules="shortNameRules"
        ></v-text-field>
      </div>
    </template>
  </inline-c-r-u-d-list>
</template>

<script>
import {
  rooms,
  createRoom,
  deleteRoom,
  deleteRooms,
  updateRooms,
} from "./room.graphql";

export default {
  name: "RoomInlineList",
  data() {
    return {
      headers: [
        {
          text: this.$t("rooms.name"),
          value: "name",
        },
        {
          text: this.$t("rooms.short_name"),
          value: "shortName",
        },
      ],
      i18nKey: "rooms",
      gqlQuery: rooms,
      gqlCreateMutation: createRoom,
      gqlPatchMutation: updateRooms,
      gqlDeleteMutation: deleteRoom,
      gqlDeleteMultipleMutation: deleteRooms,
      defaultItem: {
        name: "",
        shortName: "",
      },
      shortNameRules: [(value) => !!value || this.$t("forms.errors.required")],
    };
  },
};
</script>

<style scoped></style>
